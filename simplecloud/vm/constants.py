# -*- coding: utf-8 -*-

from flaskext.babel import lazy_gettext as _

# VM status
VM_INIT = 0
VM_INVALID = 1
VM_RUNNING = 2
VM_STOPPED = 3
VM_UNKNOWN = 4
VM_STATUS = {
    VM_INIT: _('init'),
    VM_INVALID: _('invalid'),
    VM_RUNNING: _('running'),
    VM_STOPPED: _('stopped'),
    VM_UNKNOWN: _('unknown'),
}

