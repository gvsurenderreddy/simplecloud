# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request, flash,
        redirect, url_for)
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User, USER_INACTIVE, USER_ACTIVE, USER_DELETED
from .forms import UserForm, AddUserForm
from .models import Host, Image, Task, Template


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
        flash("User " + user.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.users'))
    elif form.is_submitted():
        flash("Failed to add User", "error")    

    return render_template('admin/users.html', users=users, active='Users', form=form)

@admin.route('/hosts', methods=['GET', 'POST'])
@login_required
@admin_required
def hosts():
    hosts = Host.query.all()
    form = AddUserForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.status_code = USER_ACTIVE

        db.session.add(user)
        db.session.commit()
        flash("User " + user.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.users'))
    elif form.is_submitted():
        flash("Failed to add User", "error")    

    return render_template('admin/hosts.html', hosts=hosts, active='Hosts', form=form)

@admin.route('/images', methods=['GET', 'POST'])
@login_required
@admin_required
def images():
    images = Image.query.all()
    form = AddUserForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.status_code = USER_ACTIVE

        db.session.add(user)
        db.session.commit()
        flash("User " + user.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.users'))
    elif form.is_submitted():
        flash("Failed to add User", "error")    

    return render_template('admin/images.html', images=images, active='Images', form=form)

@admin.route('/templates', methods=['GET', 'POST'])
@login_required
@admin_required
def templates():
    templates = Template.query.all()
    form = AddUserForm(next=request.args.get('next'))

    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.status_code = USER_ACTIVE

        db.session.add(user)
        db.session.commit()
        flash("User " + user.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.users'))
    elif form.is_submitted():
        flash("Failed to add User", "error")    

    return render_template('admin/templates.html', templates=templates, active='Templates', form=form)
    
@admin.route('/storage')
@login_required
@admin_required
def storage():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Storage')

@admin.route('/network')
@login_required
@admin_required
def network():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Network')

@admin.route('/tasks')
@login_required
@admin_required
def tasks():
    tasks = Task.query.all()
    return render_template('admin/tasks.html', tasks=tasks, active='Tasks')    

@admin.route('/system')
@login_required
@admin_required
def system():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='System')        
    
@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        flash('User ' + user.name +' was updated.', 'success')
        return redirect(form.next.data or url_for('admin.users'))

    return render_template('admin/user.html', user=user, form=form)
    
@admin.route('/user/delete/<int:user_id>', methods=['GET'])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    user.status_code = USER_DELETED
    db.session.add(user)
    db.session.commit()
    flash('User '+ user.name +' was deleted.', 'success')
    return redirect(url_for('admin.users'))


