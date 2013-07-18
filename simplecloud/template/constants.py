# -*- coding: utf-8 -*-
from flaskext.babel import lazy_gettext as _

# Template status
TEMPLATE_OK = 0
TEMPLATE_INVALID = 1
TEMPLATE_STATUS = {
    TEMPLATE_OK: _('ok'),
    TEMPLATE_INVALID: _('invalid'),
}

