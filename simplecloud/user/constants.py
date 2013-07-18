# -*- coding: utf-8 -*-
from flaskext.babel import lazy_gettext as _

# User role
ADMIN = 0
USER = 1
USER_ROLE = {
    ADMIN: _('admin'),
    USER: _('user'),
}

# User status
USER_INACTIVE = 0
USER_NEW = 1
USER_ACTIVE = 2
USER_DELETED = 3
USER_STATUS = {
    USER_INACTIVE: _('inactive'),
    USER_NEW: _('new'),
    USER_ACTIVE: _('active'),
    USER_DELETED: _('deleted'),
}

# User Locale
USER_LOCALE_LEN = 10
USER_LOCALE_EN = "en"
USER_LOCALE_ZH_CN = "zh_CN"
