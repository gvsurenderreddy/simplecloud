# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime
from flaskext.babel import gettext as _

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user

from ..extensions import db
from .models import Task

task = Blueprint('task', __name__, url_prefix='/tasks')

@task.route('/')
@login_required
def index():
    tasks = Task.query.all()
    return render_template('task/index.html', tasks=tasks, active=_('Tasks'))    

