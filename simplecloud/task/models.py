# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.ext.mutable import Mutable

from ..extensions import db
from ..utils import get_current_time, STRING_LEN
from .constants import (TASK_STATUS, TASK_RUNNING)

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
