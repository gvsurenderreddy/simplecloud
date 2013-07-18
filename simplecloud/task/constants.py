# -*- coding: utf-8 -*-
from flaskext.babel import lazy_gettext as _

# Task status
TASK_RUNNING = 0
TASK_SUCCESS = 1
TASK_FAILED = 2
TASK_STATUS = {
    TASK_RUNNING: _('running'),
    TASK_SUCCESS: _('success'),
    TASK_FAILED: _('failed'),
}


