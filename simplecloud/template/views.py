# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime
from ..decorators import admin_required

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user
from flaskext.babel import gettext as _

from ..extensions import db
from .models import Template
from .forms import AddTemplateForm, AddVMForm
from ..task import log_task
from ..image import Image

template = Blueprint('template', __name__, url_prefix='/templates')

@template.route('/', methods=['GET', 'POST'])
@login_required
def index():
    templates = Template.query.filter().all()
    
    form = AddVMForm(next=request.args.get('next'))
    form.template_id.choices = Template.get_templates_choices()
    
    if current_user.is_admin():
        form = AddTemplateForm(next=request.args.get('next'))
        form.image_id.choices = Image.get_images_choices()
        
    if form.validate_on_submit():
        template = Template()
        form.populate_obj(template)
        db.session.add(template)
        db.session.commit()
        log_task(_("Add Template %(name)s", name = template.name))
        flash(_("Template %(name)s was added.", name = template.name), "success")
        return redirect(form.next.data or url_for('template.index'))
    elif form.is_submitted():
        flash(_("Failed to add Template"), "error")    

    return render_template('template/index.html', templates=templates, active=_('Templates'), form=form)

# Delete Template Page    
@template.route('/delete/<int:template_id>', methods=['GET'])
@login_required
@admin_required
def delete(template_id):
    template = Template.query.filter_by(id=template_id).first_or_404()
    
    # validate template coult be deleted
    current_app.logger.info("Try to delete template %d %s" % (template.id, str(template.vms)))
    if len(template.vms) > 0:
        errmsg = _("Couldn't delete template %(name)s with %(count)d vms using it.",
                name = template.name, count = len(template.vms))
        current_app.logger.error(errmsg)
        flash(errmsg, 'error')
        return redirect(url_for("template.index"))
        
    db.session.delete(template)
    db.session.commit()
    message = _("Delete Template %(name)s (%(id)d)", name = template.name, id = template_id)
    log_task(message)    
    flash(_('Template %(name)s was deleted.', name = template.name), 'success')
    return redirect(url_for('template.index'))

