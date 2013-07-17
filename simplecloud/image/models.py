# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from .constants import (IMAGE_STATUS, IMAGE_OK, PATH_STRING_LEN,
        IMAGE_TYPE, IMAGE_QCOW2)
from ..utils import STRING_LEN

class Image(db.Model):

    __tablename__ = 'images'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)
    src_path = Column(db.String(PATH_STRING_LEN), nullable=False, unique=False)
    templates = db.relationship("Template")

    status_code = Column(db.SmallInteger, default=IMAGE_OK)

    @property
    def status(self):
        return IMAGE_STATUS[self.status_code]
    
    type_code = Column(db.SmallInteger, default=IMAGE_QCOW2)

    @property
    def disk_format(self):
        return IMAGE_TYPE[self.type_code]
    


