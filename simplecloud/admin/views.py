# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request, flash,
        redirect, url_for)
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User, USER_ACTIVE, USER_DELETED
from .forms import AddUserForm, EditUserForm
from ..task import log_task

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='Dashboard')


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
        log_task("Add User " + user.name)
        flash("User " + user.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.users'))
    elif form.is_submitted():
        flash("Failed to add User", "error")    

    return render_template('admin/users.html', users=users, active='Users', form=form)

@admin.route('/storage')
@login_required
@admin_required
def storage():
    storage = {}
    
    storage['Type'] = "Shared Storage"
    storage['Protocol'] = "NFS"
    storage['URL'] = "testserver:/nfs"
    storage['Status'] = "OK"
    storage['Space'] = "100G"
    storage['Used'] = "50G"
    storage['Free'] = "50G"
    storage['Image Space'] = "5G"
    storage['VM Space'] = "45G"
    return render_template('admin/system.html', storage=storage, active='Storage')

@admin.route('/network')
@login_required
@admin_required
def network():
    network = {}
    network['VM Network Mode'] = "Bridge"
    network['Bridge Name'] = "br0"
    network['VM IP Mode'] = "DHCP"

    return render_template('admin/system.html', network=network, active='Network')

@admin.route('/system')
@login_required
@admin_required
def system():
    system = {}
    return render_template('admin/system.html', system=system, active='System')        

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
        message = "Update User " + user.name + "(" + str(user_id) + ")"
        log_task(message)
        flash('User ' + user.name +' was updated.', 'success')
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
    message = "Delete User " + user.name + "(" + str(user_id) + ")"
    log_task(message)
    flash('User '+ user.name +' was deleted.', 'success')
    return redirect(url_for('admin.users'))

