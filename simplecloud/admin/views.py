# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request, flash,
        redirect, url_for)
from flask.ext.login import login_required
from flaskext.babel import gettext as _
from flaskext.babel import refresh

from ..extensions import db
from ..decorators import admin_required

from ..user import User, USER_ACTIVE, USER_DELETED
from .forms import AddUserForm, EditUserForm
from ..task import log_task
from .utils import get_system_stat, get_storage_stat, get_network_stat, get_host_stat

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    refresh()
    stat = get_system_stat()
    return render_template('admin/index.html', stat=stat, active=_('Dashboard'))


@admin.route('/users', methods=['GET', 'POST'])
@login_required
@admin_required
def users():
    users = User.query.filter(User.status_code!=USER_DELETED).all()
    form = AddUserForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.status_code = USER_ACTIVE

        db.session.add(user)
        db.session.commit()
        log_task(_("Add User %(name)s", name = user.name))
        flash(_("User %(name)s was added.", name=user.name), "success")
        return redirect(form.next.data or url_for('admin.users'))
    elif form.is_submitted():
        flash(_("Failed to add User"), "error")    

    return render_template('admin/users.html', users=users, active=_('Users'), form=form)

@admin.route('/system')
@login_required
@admin_required
def system():
    host = get_host_stat()
    storage = get_storage_stat()
    network = get_network_stat()
    return render_template('admin/system.html', host=host, network=network, storage=storage, active=_('System'))

# Edit User Page    
@admin.route('/users/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = EditUserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()    
        message = _("Update User %(name)s (%(id)d)", name=user.name, id=user.id)
        log_task(message)
        flash(_('User %(name)s was updated', name=user.name), 'success')
        return redirect(form.next.data or url_for('admin.users'))

    return render_template('admin/user.html', user=user, form=form)

# Delete User    
@admin.route('/users/delete/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    user.status_code = USER_DELETED
    db.session.add(user)
    db.session.commit()
    message = _("Delete User %(name)s (%(id)d)", name=user.name, id=user.id)
    log_task(message)
    flash(_('User %(name)s was deleted.', name=user.name), 'success')
    return redirect(url_for('admin.users'))

