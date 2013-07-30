# -*- coding: utf-8 -*-

import os
import os.path
import hashlib
import shutil

from flaskext.babel import gettext as _
from datetime import datetime
from ..decorators import admin_required

from flask import (Blueprint, render_template, current_app, request, flash,
        redirect, url_for)
from flask.ext.login import login_required, current_user

from ..extensions import db
from .models import Image
from .constants import IMAGE_OK, IMAGE_INVALID
from .forms import AddImageForm
from ..task import log_task
from ..utils import IMAGE_POOL_PATH

image= Blueprint('image', __name__, url_prefix='/images')

@image.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    images = Image.query.filter().all()
    
    # Update invalid status for images with valid files
    for image in images:
        if image.status_code == IMAGE_INVALID:
            if os.path.isfile(os.path.join(IMAGE_POOL_PATH, image.name)):
                image.status_code = IMAGE_OK
                db.session.add(image)
                db.session.commit()
        elif image.status_code == IMAGE_OK:
            if not os.path.isfile(os.path.join(IMAGE_POOL_PATH, image.name)):
                image.status_code = IMAGE_INVALID
                db.session.add(image)
                db.session.commit()
    
    images = Image.query.filter().all()
    form = AddImageForm(next=request.args.get('next'))

    if form.validate_on_submit():
        image = Image()
        form.populate_obj(image)
        image.status_code = IMAGE_INVALID
        # async image copy task
        from multiprocessing import Process
        p = Process(target=copy_image,args=(image,))
        p.start()
        #copy_image(image)
        db.session.add(image)
        db.session.commit()
        message = _("Add Image %(name)s", name = image.name)
        log_task(message)
        flash(_("Image %(name)s was added.", name = image.name), "success")
        return redirect(form.next.data or url_for('image.index'))
    elif form.is_submitted():
        flash(_("Failed to add Image"), "error")    

    return render_template('image/index.html', images=images, active=_('Images'), form=form)

# Delete Image Page    
@image.route('/delete/<int:image_id>', methods=['GET'])
@login_required
@admin_required
def delete(image_id):
    image = Image.query.filter_by(id=image_id).first_or_404()

    # validate image coult be deleted
    current_app.logger.info("Try to delete image %d %s" % (image.id, str(image.templates)))
    if len(image.templates) > 0:
        errmsg = _("Couldn't delete image %(name)s with %(count)d templates using it.",
                name = image.name, count = len(image.templates))
        current_app.logger.error(errmsg)
        flash(errmsg, 'error')
        return redirect(url_for("image.index"))
        
    delete_image(image)
    db.session.delete(image)
    db.session.commit()
    message = _("Delete Image %(name)s (%(id)d)", name = image.name, id = image_id)
    log_task(message)
    flash(_('Image %(name)s was deleted.', name = image.name), 'success')
    return redirect(url_for('image.index'))

def copy_image(image):
    tmp_file = os.path.join(IMAGE_POOL_PATH, "%s.tmp" % image.name)
    dst_path = os.path.join(IMAGE_POOL_PATH, image.name)
    shutil.copy(image.src_path, tmp_file)
    shutil.move(tmp_file, dst_path)

def delete_image(image):
    try:
        src_path = os.path.join(IMAGE_POOL_PATH, image.name)
        dst_path = os.path.join(IMAGE_POOL_PATH, "%s.DELETED" % image.name)
        shutil.move(src_path, dst_path)
    except Exception, ex:
        current_app.logger.error("Failed to delete image: %s" % str(ex))




