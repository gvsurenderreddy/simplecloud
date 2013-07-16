# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from .constants import (TEMPLATE_STATUS, TEMPLATE_OK)
from ..utils import STRING_LEN

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


