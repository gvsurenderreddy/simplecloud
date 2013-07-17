# -*- coding: utf-8 -*-

from .views import host
from .models import Host
from .constants import (HOST_STATUS, HOST_OK, HOST_ERROR,
        HOST_TYPE, HOST_XEN, HOST_KVM, VM_VCPU_VALUE, HOST_CPU_VALUE)
from .utils import get_host
