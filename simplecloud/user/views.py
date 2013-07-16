# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, render_template, send_from_directory, abort,
        redirect, url_for)
from flask import current_app as APP
from flask.ext.login import login_required, current_user
from ..extensions import db
from ..decorators import admin_required

from .models import User
from ..vm import vm

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET'])
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    return redirect(url_for('vm.index'))

@user.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    user = User.get_by_id(user_id)
    return render_template('user/profile.html', user=user)


