# -*- coding: utf-8 -*-

import os

from flask import Blueprint, render_template, send_from_directory, abort
from flask import current_app as APP
from flask.ext.login import login_required, current_user
from ..extensions import db

from .models import User, VM
from .constants import VM_DELETED
#from ..admin.models import TemplateTEMPLATE_DELETED

user = Blueprint('user', __name__, url_prefix='/user')


@user.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if not current_user.is_authenticated():
        abort(403)
    vms = VM.query.filter(db.and_(VM.owner_id == current_user.id,
            VM.status_code!=VM_DELETED)).all()
    templates = Template.query.filter(Template.status_code!=TEMPLATE_DELETED).all()
    form = AddVMForm(next=request.args.get('next'))

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
      
    return render_template('user/index.html', user=current_user, templates=templates, form=form)


@user.route('/<int:user_id>/profile')
@login_required
def profile(user_id):
    user = User.get_by_id(user_id)
    return render_template('user/profile.html', user=user)


