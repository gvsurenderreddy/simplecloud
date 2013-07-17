# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from ..utils import get_current_time, STRING_LEN
from .constants import (VM_STATUS, VM_INIT)

class VM(db.Model):

    __tablename__ = 'vms'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=False)
    owner_id = Column(db.Integer, db.ForeignKey("users.id"))
    template_id = Column(db.Integer, db.ForeignKey("templates.id", ondelete="SET NULL"))
    
    host_id = Column(db.Integer, db.ForeignKey("hosts.id", ondelete="SET NULL"))
    vnc_link = Column(db.String(STRING_LEN), nullable=True, unique=False)
    created_time = Column(db.DateTime, default=get_current_time)

    status_code = Column(db.SmallInteger, default=VM_INIT)
    @property
    def status(self):
        return VM_STATUS[self.status_code]

