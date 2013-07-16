# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable
from ..extensions import db
from .constants import (IMAGE_STATUS, IMAGE_OK)
from ..utils import STRING_LEN

class Image(db.Model):

    __tablename__ = 'images'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String(STRING_LEN), nullable=False, unique=True)

    status_code = Column(db.SmallInteger, default=IMAGE_OK)

    @property
    def status(self):
        return IMAGE_STATUS[self.status_code]
    


