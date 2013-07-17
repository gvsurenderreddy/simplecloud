# -*- coding: utf-8 -*-

from flask import current_app, flash
from flask.ext.login import current_user
from .models import Task
from .constants import TASK_SUCCESS, TASK_FAILED, TASK_STATUS
from ..extensions import db

def old_log_task(name, status=TASK_SUCCESS):
    current_app.logger.info("%s: status=%s" % (name, TASK_STATUS[status]))
    task = Task(name=name, owner_id=current_user.id, status_code=status)
    db.session.add(task)
    db.session.commit()
    
def log_task(name, status=TASK_SUCCESS, message=None):
    current_app.logger.info("%s: status=%s" % (name, TASK_STATUS[status]))
    task = Task(name=name, owner_id=current_user.id, status_code=status)
    db.session.add(task)
    db.session.commit()
    
    if status == TASK_SUCCESS and message:
        flash(message, "success")
    
    if status == TASK_FAILED and message:
        flash(message, "error")
    
