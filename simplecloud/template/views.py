# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime
from ..decorators import admin_required

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user

from ..extensions import db
from .models import Template
from .forms import AddTemplateForm, AddVMForm
from ..task import log_task

template = Blueprint('template', __name__, url_prefix='/templates')

@template.route('/', methods=['GET', 'POST'])
@login_required
def index():
    templates = Template.query.filter().all()
    
    form = AddVMForm(next=request.args.get('next'))
    if current_user.is_admin():
        form = AddTemplateForm(next=request.args.get('next'))
        
    if form.validate_on_submit():
        template = Template()
        form.populate_obj(template)
        db.session.add(template)
        db.session.commit()
        log_task("Add Template " + template.name)
        flash("Template " + template.name + " was added.", "success")
        return redirect(form.next.data or url_for('template.index'))
    elif form.is_submitted():
        flash("Failed to add Template", "error")    

    return render_template('template/index.html', templates=templates, active='Templates', form=form)

# Delete Template Page    
@template.route('/delete/<int:template_id>', methods=['GET'])
@login_required
@admin_required
def delete(template_id):
    template = Template.query.filter_by(id=template_id).first_or_404()
    
    # validate template coult be deleted
    current_app.logger.info("Try to delete template %d %s" % (template.id, str(template.vms)))
    if len(template.vms) > 0:
        errmsg = "Couldn't delete template %s with %d vms using it." % (template.name, len(template.vms))
        current_app.logger.error(errmsg)
        flash(errmsg, 'error')
        return redirect(url_for("template.index"))
        
    db.session.delete(template)
    db.session.commit()
    message = "Delete Template " + template.name+ "(" + str(template_id) + ")"
    log_task(message)    
    flash('Template '+ template.name +' was deleted.', 'success')
    return redirect(url_for('template.index'))

