# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable

from ..extensions import db
from ..utils import get_current_time
from .constants import (TASK_STATUS, TASK_RUNNING, IMAGE_STATUS,
        IMAGE_OK, TEMPLATE_STATUS, TEMPLATE_OK, HOST_STATUS, 
        HOST_OK, HOST_TYPE, HOST_KVM, HOST_XEN)
from ..user import STRING_LEN

class Task(db.Model):

    __tablename__ = 'tasks'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False)
    owner_id = Column(db.Integer, db.ForeignKey("users.id"))
    created_time = Column(db.DateTime, default=get_current_time)

    # ================================================================
    # One-to-many relationship between tasks and task_statuses.
    status_code = Column(db.SmallInteger, default=TASK_RUNNING)

    @property
    def status(self):
        return TASK_STATUS[self.status_code]

class Image(db.Model):

    __tablename__ = 'images'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)

    status_code = Column(db.SmallInteger, default=IMAGE_OK)

    @property
    def status(self):
        return IMAGE_STATUS[self.status_code]
        
class Template(db.Model):

    __tablename__ = 'templates'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    image_id = Column(db.Integer, db.ForeignKey("images.id"))
    
    # VCPU number
    vcpu = Column(db.Integer, nullable=False)
    # Memory size (M)
    memory = Column(db.Integer, nullable=False)
    # Disk size (M)
    disk = Column(db.Integer, nullable=False)
    # The number of VM created from this template
    vm_number = Column(db.Integer, default=0)

    status_code = Column(db.SmallInteger, default=TEMPLATE_OK)

    @property
    def status(self):
        return TEMPLATE_STATUS[self.status_code]

class Host(db.Model):

    __tablename__ = 'hosts'

    id = Column(db.Integer, primary_key=True)
    address = Column(db.String(STRING_LEN), nullable=False, unique=True)
    uri = Column(db.String(STRING_LEN), nullable=False, unique=True)
    username = Column(db.String(STRING_LEN), nullable=False)
    
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
                

