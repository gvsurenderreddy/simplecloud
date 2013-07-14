# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User
from .forms import UserForm


admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    return render_template('admin/index.html', users=users, active='Dashboard')


@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Users')

@admin.route('/hosts')
@login_required
@admin_required
def hosts():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Hosts')

@admin.route('/images')
@login_required
@admin_required
def images():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Images')

@admin.route('/templates')
@login_required
@admin_required
def templates():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Templates')
    
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
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='Tasks')    

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

        flash('User updated.', 'success')

    return render_template('admin/user.html', user=user, form=form)
