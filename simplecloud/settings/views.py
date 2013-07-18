# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime

from flask import Blueprint, render_template, current_app, request, flash
from flask.ext.login import login_required, current_user
from flaskext.babel import refresh
from ..extensions import db
from ..user import User
from .forms import ProfileForm, PasswordForm
from flaskext.babel import gettext as _

settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = ProfileForm(obj=user,
            next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        #current_user.locale = user.locale
        #refresh()

        flash(_('Public profile updated.'), 'success')

    return render_template('settings/profile.html', user=user,
            active=_("profile"), form=form)


@settings.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = PasswordForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)
        user.password = form.new_password.data

        db.session.add(user)
        db.session.commit()

        flash('Password updated.', 'success')

    return render_template('settings/password.html', user=user,
            active=_("password"), form=form)
