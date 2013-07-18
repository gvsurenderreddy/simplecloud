# -*- coding: utf-8 -*-

import os.path
from .models import Image
from ..utils import IMAGE_POOL_PATH
from flaskext.babel import lazy_gettext as _

def get_image_path(image_id):
    image = Image.query.filter_by(id=image_id).first()
    if not image:
        raise Exception(_("Not found image with id %(id)d", id = image_id))
    return os.path.join(IMAGE_POOL_PATH, image.name)
