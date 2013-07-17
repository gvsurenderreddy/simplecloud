# -*- coding: utf-8 -*-

import os.path
from .models import Image
from ..utils import IMAGE_POOL_PATH

def get_image_path(image_id):
    image = Image.query.filter_by(id=image_id).first()
    if not image:
        raise Exception("Not found image with id %d" % image_id)
    return os.path.join(IMAGE_POOL_PATH, image.name)
