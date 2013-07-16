# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from .constants import (HOST_STATUS, HOST_OK, HOST_ERROR, HOST_TYPE, HOST_KVM, 
        HOST_XEN, HOST_CPU_VALUE)
from ..utils import STRING_LEN


class Host(db.Model):

    __tablename__ = 'hosts'

    id = Column(db.Integer, primary_key=True)
    address = Column(db.String(STRING_LEN), nullable=False, unique=True)
    uri = Column(db.String(STRING_LEN), nullable=False, unique=True)
    username = Column(db.String(STRING_LEN), default="root")
    
    # capability of this host
    cpu_pool = Column(db.Integer, default=0)
    cpu_used = Column(db.Integer, default=0)
    mem_pool = Column(db.Integer, default=0)
    mem_used = Column(db.Integer, default=0)
    # the number of vm running on this host
    vm_number = Column(db.Integer, default=0)
    
    type_code = Column(db.SmallInteger, default=HOST_KVM)
    @property
    def hypervisor_type(self):
        return HOST_TYPE[self.type_code]    

    status_code = Column(db.SmallInteger, default=HOST_OK)
    @property
    def status(self):
        return HOST_STATUS[self.status_code]
    
    def validate_delete(self):
        return not (self.vm_number > 0)
    
    def check_connect(self):
        # 1. generate uri
        uri = self.username + "@" + self.address + "/"
        if int(self.type_code) == HOST_XEN:
            self.uri = "xen+ssh://" + uri
        elif int(self.type_code) == HOST_KVM:
            self.uri = "qemu+ssh://" + uri + "system"
        else:
            errMsg = "Not supported hypervisor type " + str(self.type_code)
            self.status_code = HOST_ERROR
            return False,errMsg
        # 2. connect uri and get cpu_pool/mem_pool
        try:
            import libvirt
            conn = libvirt.open(self.uri)
            infolist = conn.getInfo()
            self.mem_pool = infolist[1]
            self.cpu_pool = infolist[2] * HOST_CPU_VALUE
            self.status_code = HOST_OK
            return True, ""
        except Exception, ex:
            self.status_code = HOST_ERROR
            self.mem_pool = 0
            self.cpu_pool = 0
            return False, str(ex)
            
                

    


