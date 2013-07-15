# -*- coding: utf-8 -*-

from flask import (Blueprint, render_template, request, flash,
        redirect, url_for)
from flask.ext.login import login_required

from ..extensions import db
from ..decorators import admin_required

from ..user import User, USER_INACTIVE, USER_ACTIVE, USER_DELETED
from .forms import (AddUserForm, EditUserForm, AddHostForm, EditHostForm,
        AddImageForm, AddTemplateForm)
from .models import Host, Image, Task, Template
from .constants import HOST_TYPE, HOST_KVM, HOST_XEN, IMAGE_DELETED, TEMPLATE_DELETED


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
    form = AddHostForm(next=request.args.get('next'))

    if form.validate_on_submit():
        host = Host()
        form.populate_obj(host)
        # TODO: update host object before insert to DB
        # 1. generate uri
        uri = host.username + "@" + host.address + "/"
        if int(host.type_code) == HOST_XEN:
            host.uri = "xen+ssh://" + uri
        elif int(host.type_code) == HOST_KVM:
            host.uri = "qemu+ssh://" + uri + "system"
        else:
            flash("Not supported hypervisor type " + str(host.type_code), "error")
            return redirect(form.next.data or url_for('admin.hosts'))
        # 2. connect uri and get cpu_pool/mem_pool
        # 3. init cpu_used/mem_used/vm_number as 0
        # 4. update status_code

        db.session.add(host)
        db.session.commit()
        flash("Host " + host.address + " was added.", "success")
        return redirect(form.next.data or url_for('admin.hosts'))
    elif form.is_submitted():
        flash("Failed to add Host", "error")    

    return render_template('admin/hosts.html', hosts=hosts, active='Hosts', form=form)

@admin.route('/images', methods=['GET', 'POST'])
@login_required
@admin_required
def images():
    images = Image.query.filter(Image.status_code!=IMAGE_DELETED).all()
    form = AddImageForm(next=request.args.get('next'))

    if form.validate_on_submit():
        image = Image()
        form.populate_obj(image)
        # TODO: Copy image and update image status_code

        db.session.add(image)
        db.session.commit()
        flash("Image " + image.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.images'))
    elif form.is_submitted():
        flash("Failed to add Image", "error")    

    return render_template('admin/images.html', images=images, active='Images', form=form)

@admin.route('/templates', methods=['GET', 'POST'])
@login_required
@admin_required
def templates():
    templates = Template.query.filter(Template.status_code!=TEMPLATE_DELETED).all()
    form = AddTemplateForm(next=request.args.get('next'))

    if form.validate_on_submit():
        template = Template()
        form.populate_obj(template)
        # TODO: update status_code

        db.session.add(template)
        db.session.commit()
        flash("Template " + template.name + " was added.", "success")
        return redirect(form.next.data or url_for('admin.templates'))
    elif form.is_submitted():
        flash("Failed to add Template", "error")    

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
    flash('User '+ user.name +' was deleted.', 'success')
    return redirect(url_for('admin.users'))

# Edit Host page
@admin.route('/hosts/<int:host_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def host(host_id):
    host = Host.query.filter_by(id=host_id).first_or_404()
    form = EditHostForm(obj=host, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(host)

        db.session.add(host)
        db.session.commit()

        flash('Host ' + host.address +' was updated.', 'success')
        return redirect(form.next.data or url_for('admin.hosts'))

    return render_template('admin/host.html', host=host, form=form)

# Delete Host Page    
@admin.route('/hosts/delete/<int:host_id>', methods=['GET'])
@login_required
@admin_required
def delete_host(host_id):
    host = Host.query.filter_by(id=host_id).first_or_404()
    # TODO: validation
    db.session.delete(host)
    db.session.commit()
    flash('Host '+ host.address +' was deleted.', 'success')
    return redirect(url_for('admin.hosts'))

# Delete Image Page    
@admin.route('/images/delete/<int:image_id>', methods=['GET'])
@login_required
@admin_required
def delete_image(image_id):
    image = Image.query.filter_by(id=image_id).first_or_404()
    # TODO: validation
    image.status_code = IMAGE_DELETED
    db.session.add(image)
    db.session.commit()
    flash('Image '+ image.name +' was deleted.', 'success')
    return redirect(url_for('admin.images'))
    
# Delete Template Page    
@admin.route('/templates/delete/<int:template_id>', methods=['GET'])
@login_required
@admin_required
def delete_template(template_id):
    template = Template.query.filter_by(id=template_id).first_or_404()
    # TODO: validation
    template.status_code = TEMPLATE_DELETED
    db.session.add(template)
    db.session.commit()
    flash('Template '+ template.name +' was deleted.', 'success')
    return redirect(url_for('admin.templates'))

