# -*- coding: utf-8 -*-

import os
from sqlalchemy import func
from ..user import User
from ..host import Host
from ..image import Image
from ..template import Template
from ..vm import VM, VM_RUNNING, VM_STOPPED
from ..extensions import db
from ..utils import (INSTANCE_FOLDER_PATH, SHARED_STORAGE_PATH, STORAGE_PROTOCOL,
        STORAGE_TYPE, IMAGE_POOL_PATH, VM_POOL_PATH, NETWORK_MODE, VM_NETWORK_MODE,
        NETWORK_NAME, HOST_PUBKEY_FILE)

def get_host_stat():
    host = {}
    #host['key'] = open(HOST_PUBKEY_FILE, 'r').readline()
    return host
    
def get_storage_stat():
    storage = {}    
    storage['type'] = STORAGE_TYPE
    storage['protocol'] = STORAGE_PROTOCOL
    storage['path'] = INSTANCE_FOLDER_PATH
    storage['status'] = "ERROR"
    storage['total_space'] = 0
    storage['used_space'] = 0
    storage['free_space'] = 0
    storage['image_pool'] = IMAGE_POOL_PATH
    storage['vm_pool'] = VM_POOL_PATH
    
    if os.path.isdir(INSTANCE_FOLDER_PATH):
        storage['status'] = "OK"
        vfsstat = os.statvfs(INSTANCE_FOLDER_PATH)
        blocksize = vfsstat.f_bsize
        storage['total_space'] = vfsstat.f_blocks*blocksize/(1024*1024)
        storage['free_space'] = vfsstat.f_bfree*blocksize/(1024*1024)
        storage['used_space'] = storage['total_space'] - storage['free_space']
    return storage

def get_network_stat():
    network = {}
    network['mode'] = NETWORK_MODE
    network['name'] = NETWORK_NAME
    network['vm_mode'] = VM_NETWORK_MODE
    network['status'] = "OK"
    return network

def get_system_stat():
    stat = {}
    vmstat = {}
    resourcestat = {}
    stat['users'] = User.query.count()
    stat['hosts'] = Host.query.count()
    stat['images'] = Image.query.count()
    stat['templates'] = Template.query.count()
    vmstat['total'] = VM.query.count()
    vmstat['running'] = VM.query.filter(VM.status_code == VM_RUNNING).count()
    vmstat['stopped'] = VM.query.filter(VM.status_code == VM_STOPPED).count()

    cpu_pool = db.session.query(func.sum(Host.cpu_pool)).first()[0]
    mem_pool = db.session.query(func.sum(Host.mem_pool)).first()[0]
    cpu_used = db.session.query(func.sum(Host.cpu_used)).first()[0]
    mem_used = db.session.query(func.sum(Host.mem_used)).first()[0]
    if cpu_pool is None:
        cpu_pool = 0
    
    if mem_pool is None:
        mem_pool = 0
    
    if cpu_used is None:
        cpu_used = 0
    
    if mem_used is None:
        mem_used = 0
    
    storagestat = get_storage_stat()
    resourcestat['cpu'] = 0
    resourcestat['memory'] = 0
    resourcestat['disk'] = 1
    
    if cpu_pool:
        resourcestat['cpu'] = float(cpu_used)/cpu_pool
    
    if mem_pool:
        resourcestat['memory'] = float(mem_used)/mem_pool

    if storagestat['total_space']:
        resourcestat['disk'] = float(storagestat['used_space'])/storagestat['total_space']
    
    stat['vm'] = vmstat
    stat['resource'] = resourcestat
    return stat

