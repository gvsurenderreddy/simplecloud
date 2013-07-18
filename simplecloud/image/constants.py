# -*- coding: utf-8 -*-
from flaskext.babel import lazy_gettext as _

PATH_STRING_LEN = 1024

# Image status
IMAGE_OK = 0
IMAGE_INVALID = 1
IMAGE_STATUS = {
    IMAGE_OK: _('ok'),
    IMAGE_INVALID: _('invalid'),
}

# Image type
IMAGE_QCOW2 = 0
IMAGE_RAW = 1
IMAGE_TYPE = {
    IMAGE_QCOW2: 'qcow2',
    IMAGE_RAW: 'raw',
}


