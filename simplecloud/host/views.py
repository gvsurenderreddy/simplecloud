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

from .constants import HOST_TYPE, HOST_OK, HOST_ERROR, HOST_KVM, HOST_XEN, HOST_CPU_VALUE
from ..task import log_task, TASK_FAILED

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
        status,errMsg = host.check_connect()
        message = "Add Host "+ host.address
        if status:
            flash("Host " + host.address + " was added.", "success")
            log_task(message)
        else:
            flash("Failed to add Host " + host.address, "error")
            current_app.logger.error(errMsg)
            log_task(message, TASK_FAILED)

        db.session.add(host)
        db.session.commit()        
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
        status,errMsg = host.check_connect()
        message = "Update Host "+ host.address
        if status:
            flash("Host " + host.address + " was updated.", "success")
            log_task(message)
        else:
            flash("Failed to reconnect Host " + host.address, "error")
            current_app.logger.error(errMsg)
            log_task(message, TASK_FAILED)

        db.session.add(host)
        db.session.commit()        
        return redirect(form.next.data or url_for('host.index'))

    return render_template('host/edit.html', host=host, form=form)

# Delete Host Page    
@host.route('/delete/<int:host_id>', methods=['GET'])
@login_required
@admin_required
def delete(host_id):
    host = Host.query.filter_by(id=host_id).first_or_404()

    if not host.validate_delete():
        flash("Some VirtualMachine is on this Host, Couldn't be deleted", "error")
        return redirect(url_for('host.index'))
    db.session.delete(host)
    db.session.commit()
    message = "Delete Host " + host.address + "(" + str(host_id) + ")"
    log_task(message)
    flash('Host '+ host.address +' was deleted.', 'success')
    return redirect(url_for('host.index'))

