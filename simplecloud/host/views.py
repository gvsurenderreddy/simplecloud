# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime
from ..decorators import admin_required

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user

from ..extensions import db
from .models import Host
from .forms import AddHostForm, EditHostForm

from .constants import HOST_TYPE, HOST_KVM, HOST_XEN
from ..task import log_task

host = Blueprint('host', __name__, url_prefix='/hosts')

@host.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
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
        message = "Add Host "+ host.address
        log_task(message)
        flash("Host " + host.address + " was added.", "success")
        return redirect(form.next.data or url_for('host.index'))
    elif form.is_submitted():
        flash("Failed to add Host", "error")    

    return render_template('host/index.html', hosts=hosts, active='Hosts', form=form)

# Edit Host page
@host.route('/edit/<int:host_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(host_id):
    host = Host.query.filter_by(id=host_id).first_or_404()
    form = EditHostForm(obj=host, next=request.args.get('next'))

    if form.validate_on_submit():
        form.populate_obj(host)

        db.session.add(host)
        db.session.commit()
        message = "Update Host " + host.address + "(" + str(host_id) + ")"
        log_task(message)
        flash('Host ' + host.address +' was updated.', 'success')
        return redirect(form.next.data or url_for('host.index'))

    return render_template('host/edit.html', host=host, form=form)

# Delete Host Page    
@host.route('/delete/<int:host_id>', methods=['GET'])
@login_required
@admin_required
def delete(host_id):
    host = Host.query.filter_by(id=host_id).first_or_404()
    # TODO: validation
    db.session.delete(host)
    db.session.commit()
    message = "Delete Host " + host.address + "(" + str(host_id) + ")"
    log_task(message)
    flash('Host '+ host.address +' was deleted.', 'success')
    return redirect(url_for('host.index'))

