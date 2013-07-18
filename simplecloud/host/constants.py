# -*- coding: utf-8 -*-
from flaskext.babel import lazy_gettext as _

VM_VCPU_VALUE = 50
HOST_CPU_VALUE = 100

# Host status
HOST_OK = 0
HOST_ERROR = 1
HOST_STATUS = {
    HOST_OK: _('ok'),
    HOST_ERROR: _('error'),
}

# Host Hypervisor Type
HOST_XEN = 0
HOST_KVM = 1
HOST_TYPE = {
    HOST_XEN: 'xen',
    HOST_KVM: 'kvm',
}



