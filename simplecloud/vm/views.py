# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user

from ..extensions import db
from .models import VM
from .forms import AddVMForm
from ..task import log_task

vm = Blueprint('vm', __name__, url_prefix='/vms')


@vm.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    if current_user.is_admin():
        vms = VM.query.filter().all()
    else:
        vms = VM.query.filter(VM.owner_id == current_user.id).all()

    form = AddVMForm(next=request.args.get('next'))

    if form.validate_on_submit():
        vm = VM()
        form.populate_obj(vm)
        # validate VM name here
        if VM.query.filter(db.and_(VM.owner_id == current_user.id,
                VM.name == vm.name)).first() is not None:
            flash("VM Name %s is taken." % vm.name, "error")
            return redirect(form.next.data or url_for('user.index'))
        vm.owner_id = current_user.id
        # Find host
        # vm.host_id = 
        
        
        # TODO: Start VM

        db.session.add(vm)
        db.session.commit()
        log_task("Add VM " + vm.name)
        flash("VM " + vm.name + " was added.", "success")
        return redirect(form.next.data or url_for('vm.index'))
    elif form.is_submitted():
        flash("Failed to add VM", "error")
      
    return render_template('vm/index.html', vms=vms, form=form, active="VirtualMachines")
    
# Delete VM Page    
@vm.route('/delete/<int:vm_id>', methods=['GET'])
@login_required
def delete(vm_id):
    vm = VM.query.filter_by(id=vm_id).first_or_404()
    # TODO: validation
    # TODO: Libvirt Delete VM
    db.session.delete(vm)
    db.session.commit()
    message = "Delete VM " + vm.name + "(" + str(vm_id) + ")"
    log_task(message)
    flash('VM '+ vm.name +' was deleted.', 'success')
    return redirect(url_for('vm.index'))
