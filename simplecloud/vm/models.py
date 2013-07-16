# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from ..utils import get_current_time, STRING_LEN
from .constants import (VM_STATUS, VM_OK)

class VM(db.Model):

    __tablename__ = 'vms'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=False)
    owner_id = Column(db.Integer, db.ForeignKey("users.id"))
    template_id = Column(db.Integer, db.ForeignKey("templates.id"))
    # host_id = Column(db.Integer, nullable=True, db.ForeignKey("hosts.id"))
    host_id = Column(db.Integer, nullable=True)
    created_time = Column(db.DateTime, default=get_current_time)

    status_code = Column(db.SmallInteger, default=VM_OK)
    @property
    def status(self):
        return VM_STATUS[self.VM_code]

