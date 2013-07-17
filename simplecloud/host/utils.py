# -*- coding: utf-8 -*-

from flask import current_app
from flask.ext.login import current_user
from .models import Host
from .constants import HOST_OK
from ..extensions import db

# Get the target host for new created VM
def get_host(cpu_require, mem_require):
    current_app.logger.info("Searching host for cpu %d mem %dM" % (cpu_require, mem_require))
    target_host = None
    hosts = Host.query.filter(Host.status_code == HOST_OK).all()
    for host in hosts:
        # overcommitment not allowed
        free_cpu = host.cpu_pool - host.cpu_used
        free_mem = host.mem_pool - host.mem_used
        
        current_app.logger.info("Check host %d with free cpu %d free mem %d" %
                (host.id, free_cpu, free_mem))
        if free_cpu < cpu_require:
            continue

        if free_mem < mem_require:
            continue
        
        # Find the host with most cpu-value
        if not target_host:
            current_app.logger.info("Found one host %d" % host.id)
            target_host = host
            continue

        if (target_host.cpu_pool - target_host.cpu_used) < free_cpu:
            target_host = host
    
    if not target_host:
        current_app.logger.error("No available host is found.")
        raise Exception("No available host is found.")
    
    return target_host.id
