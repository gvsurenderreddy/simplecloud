# -*- coding: utf-8 -*-

from lxml import etree
import os.path
import libvirt
from subprocess import check_call
import shutil

from flask import current_app, flash
from flask.ext.login import current_user
from ..extensions import db
from ..template import Template
from ..host import get_host, Host
from ..image import get_image_path
from ..utils import VM_POOL_PATH, get_xml_file
from ..task import log_task, TASK_FAILED, TASK_SUCCESS
from .constants import VM_RUNNING, VM_STOPPED, VM_UNKNOWN
from flaskext.babel import gettext as _

KVM_VM_TEMPLATE_XML = """
<domain type='kvm'>
  <name>%s</name>
  <vcpu>%s</vcpu>  
  <memory unit='MB'>%s</memory>
  <os>
    <type arch='x86_64' machine='pc-i440fx-1.4'>hvm</type>
    <boot dev='hd'/>
  </os>
  <features>
    <acpi/>
    <apic/>
    <pae/>
  </features>
  <clock offset='utc'/>
  <on_poweroff>destroy</on_poweroff>
  <on_reboot>restart</on_reboot>
  <on_crash>restart</on_crash>
  <devices>
    <emulator>/usr/bin/kvm-spice</emulator>
    <disk type='file' device='disk'>
      <driver name='qemu' type='qcow2'/>
      <source file='%s'/>
      <target dev='hda' bus='ide'/>
      <address type='drive' controller='0' bus='0' target='0' unit='0'/>
    </disk>
    <interface type='network'>
      <source network='default'/>
    </interface>
    <graphics type='vnc' port='-1' autoport='yes'/>
    <memballoon model='virtio'>
      <address type='pci' domain='0x0000' bus='0x00' slot='0x05' function='0x0'/>
    </memballoon>
  </devices>
</domain>
"""

def get_vm_realname(user_id, name):
    return "%s-%s" % (str(user_id), name)

def get_vm_disk(user_id, vmname):
    disk_file = "%s-%s.qcow2" % (str(user_id), vmname)
    return os.path.join(VM_POOL_PATH, disk_file)

def get_vm_xml(vmname, cpu, mem, disk_path):
    try:
	xml_file = get_xml_file()
	return xml_file % (vmname, cpu, mem, disk_path)
    except Exception, ex:
	current_app.logger.error("Failed to get xml from config file: %s" % str(ex))
    	return KVM_VM_TEMPLATE_XML % (vmname, cpu, mem, disk_path)

def get_libvirt_connection(vm):
    host =  Host.query.filter_by(id=vm.host_id).first()
    
    if not host:
        raise Exception(_("Not found host with id %(id)d", id = vm.host_id))
    
    return libvirt.open(host.uri)

def get_libvirt_domain(vm):
    con = get_libvirt_connection(vm)
    name = get_vm_realname(vm.owner_id, vm.name)
    return con.lookupByName(name)

def create_vm_disk(path, size, backing_file):
    cmd = "qemu-img create -f qcow2 %s -b %s -o size=%sM" % (path, backing_file, size)
    check_call(cmd, shell=True)

def delete_vm_disk(vm):
    disk_path = get_vm_disk(vm.owner_id, vm.name)
    # TODO: Delete VM disk
    shutil.move(disk_path, "%s.DELETED" % disk_path)

def get_vm_vnclink(vm):
    host = Host.query.filter_by(id=vm.host_id).first()
        
    if not host:
        raise Exception(_("Not found host with id %(id)d", id = vm.host_id))
    
    con = libvirt.open(host.uri)
    name = get_vm_realname(vm.owner_id, vm.name)
    dom = con.lookupByName(name)
    xml = dom.XMLDesc(libvirt.VIR_DOMAIN_XML_SECURE)
    root = etree.XML(xml)
    vncElements = root.findall(".//graphics")
    port = "-1"
    for vncElement in vncElements:
        if vncElement.get('type') == 'vnc':
            port = vncElement.get('port')    
            break

    return "%s:%s" % (host.address, port) 

# Create new VM with template
def create_vm(vm):
    try:
        template = Template.query.filter_by(id=vm.template_id).first()
        if not template:
            raise Exception(_("Not found template with id %(id)d", id = vm.template_id))
        # 1. Get available Host       
        vm.host_id = get_host(template.pcpu, template.memory)
        host = Host.query.filter_by(id=vm.host_id).first()
        
        if not host:
            raise Exception(_("Not found host with id %(id)d", id = vm.host_id))

        # 2. Create the VM disk
        disk_path = get_vm_disk(vm.owner_id, vm.name)
        image_path = get_image_path(template.image_id)
        create_vm_disk(disk_path, template.disk, image_path)
        
        # 3. Generate the VM XML configfile   
        realname = get_vm_realname(vm.owner_id, vm.name)
        vm_xml = get_vm_xml(realname, template.vcpu, template.memory, disk_path)
        
        # 4. Boot up VM
        con = get_libvirt_connection(vm)
        dom = con.defineXML(vm_xml)
        dom.create()
        
        vm.status_code = VM_RUNNING
        
        vm.vnc_link = get_vm_vnclink(vm)
        
        # 5. Update DB
        # Update Host/Template/VM
        db.session.add(vm)
        
        host.vm_number = host.vm_number + 1
        host.cpu_used = host.cpu_used + template.pcpu
        host.mem_used = host.mem_used + template.memory
        db.session.add(host)
        
        template.vm_number = template.vm_number + 1
        db.session.add(template)
         
        db.session.commit()
        
        
        message = _("VM %(name)s was added.", name = vm.name)
        log_task("Add VM %s " % vm.name, TASK_SUCCESS, message)
    except Exception, ex:
        errMsg = _("Failed to create VM %(name)s: %(error)s", name = vm.name, error = str(ex))
        log_task(_("Add VM %(name)s", name = vm.name), TASK_FAILED, errMsg)


class VMAction:
    # Delete VM
    def delete(self, vm):
        try:
            # 1. Get the VM
            dom = get_libvirt_domain(vm)
            
            # 2. stop VM if running
            if vm.status_code == VM_RUNNING and dom.isActive():
                dom.destroy()
            
            # 3. delete VM disk
            delete_vm_disk(vm)
            
            # 4. undefine VM
            dom.undefine()
            
            # 5. update DB
            # Update Host/Template/VM
            
            template = Template.query.filter_by(id=vm.template_id).first()
            
            if not template:
                raise Exception(_("Not found template with id %(id)d", id = vm.template_id))
            template.vm_number = template.vm_number - 1      
            db.session.add(template)
            
            host = Host.query.filter_by(id=vm.host_id).first()
        
            if not host:
                raise Exception(_("Not found host with id %(id)d", id = vm.host_id))
            host.vm_number = host.vm_number - 1
            host.cpu_used = host.cpu_used - template.pcpu
            host.mem_used = host.mem_used - template.memory
            db.session.add(host)

            
            db.session.delete(vm)
            db.session.commit()
            
            message = _("Delete VM %(name)s (%(id)d)", name = vm.name, id = vm.id)
            log_task(message)
            flash(_('VM %(name)s was deleted.', name = vm.name), 'success')        
        except Exception, ex:
            errMsg = _("Failed to delete VM %(name)s: %(error)s", name = vm.name, error = str(ex))
            log_task(_("Delete VM %(name)s (%(id)d)", name = vm.name, id = vm.id), TASK_FAILED, errMsg)

    def start(self, vm):
        try:
            # 1. Get the VM
            dom = get_libvirt_domain(vm)
            
            # 2. start VM if not running
            if not dom.isActive():
                dom.create()
            
            vm.status_code = VM_RUNNING
            db.session.add(vm)
            db.session.commit()
            message = _("Start VM %(name)s (%(id)d)", name = vm.name, id = vm.id)
            log_task(message)
            flash(_('VM %(name)s was started.', name = vm.name), 'success')        
        except Exception, ex:
            errMsg = _("Failed to start VM %(name)s: %(error)s", name = vm.name, error = str(ex))
            log_task(_("Start VM %(name)s (%(id)d)", name = vm.name, id = vm.id), TASK_FAILED, errMsg)

    def shutdown(self, vm):
        try:
            # 1. Get the VM
            dom = get_libvirt_domain(vm)
            
            # 2. shutdown VM if running
            if dom.isActive():
                dom.shutdown()
            message = _("Shutdown VM %(name)s (%(id)d)", name = vm.name, id = vm.id)
            log_task(message)
            flash(_('VM %(name)s was shutdown.', name = vm.name), 'success')        
        except Exception, ex:
            errMsg = _("Failed to shutdown VM %(name)s: %(error)s", name = vm.name, error = str(ex))
            log_task(_("Shutdown VM %(name)s (%(id)d)", name = vm.name, id = vm.id), TASK_FAILED, errMsg)

    def stop(self, vm):
        try:
            # 1. Get the VM
            dom = get_libvirt_domain(vm)
            
            # 2. stop VM if running
            if dom.isActive():
                dom.destroy()
            vm.status_code = VM_STOPPED
            db.session.add(vm)
            db.session.commit()
            message = _("Stop VM %(name)s (%(id)d)", name = vm.name, id = vm.id)
            log_task(message)
            flash(_('VM %(name)s was stopped.', name = vm.name), 'success')        
        except Exception, ex:
            errMsg = _("Failed to stop VM %(name)s: %(error)s", name = vm.name, error = str(ex))
            log_task(_("Stop VM %(name)s (%(id)d)", name = vm.name, id = vm.id), TASK_FAILED, errMsg)

    def reboot(self, vm):
        try:
            dom = get_libvirt_domain(vm)
            dom.reboot(0)
            vm.status_code = VM_RUNNING
            db.session.add(vm)
            db.session.commit()
            message = _("Reboot VM %(name)s (%(id)d)", name = vm.name, id = vm.id)
            log_task(message)
            flash(_('VM %(name)s was rebooted.', name = vm.name), 'success')        
        except Exception, ex:
            errMsg = _("Failed to reboot VM %(name)s: %(error)s", name = vm.name, error = str(ex))
            log_task(_("Reboot VM %(name)s (%(id)d)", name = vm.name, id = vm.id), TASK_FAILED, errMsg)
    

