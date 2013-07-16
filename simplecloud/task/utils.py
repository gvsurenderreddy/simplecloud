# -*- coding: utf-8 -*-

from flask.ext.login import current_user
from .models import Task
from .constants import TASK_SUCCESS, TASK_FAILED
from ..extensions import db

def log_task(name, status=TASK_SUCCESS):
    task = Task(name=name, owner_id=current_user.id, status_code=status)
    db.session.add(task)
    db.session.commit()

