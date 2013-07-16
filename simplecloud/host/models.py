# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from .constants import (HOST_STATUS, HOST_OK, HOST_TYPE, HOST_KVM, HOST_XEN)
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
                

    


