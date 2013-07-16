# -*- coding: utf-8 -*-

import os
import hashlib

from datetime import datetime
from ..decorators import admin_required

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user

from ..extensions import db
from .models import Image
from .constants import IMAGE_DELETED
from .forms import AddImageForm


image= Blueprint('image', __name__, url_prefix='/images')

@image.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
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

    return render_template('image/index.html', images=images, active='Images', form=form)

# Delete Image Page    
@image.route('/delete/<int:image_id>', methods=['GET'])
@login_required
@admin_required
def delete(image_id):
    image = Image.query.filter_by(id=image_id).first_or_404()
    # TODO: validation
    image.status_code = IMAGE_DELETED
    db.session.add(image)
    db.session.commit()
    flash('Image '+ image.name +' was deleted.', 'success')
    return redirect(url_for('image.index'))
