# -*- coding: utf-8 -*-

# Task status
TASK_RUNNING = 0
TASK_SUCCESS = 1
TASK_FAILED = 2
TASK_STATUS = {
    TASK_RUNNING: 'running',
    TASK_SUCCESS: 'success',
    TASK_FAILED: 'failed',
}

# Image status
IMAGE_OK = 0
IMAGE_INVALID = 1
IMAGE_DELETED = 2
IMAGE_STATUS = {
    IMAGE_OK: 'ok',
    IMAGE_INVALID: 'invalid',
    IMAGE_DELETED: 'deleted',
}

# Template status
TEMPLATE_OK = 0
TEMPLATE_INVALID = 1
TEMPLATE_DELETED = 2
TEMPLATE_STATUS = {
    TEMPLATE_OK: 'ok',
    TEMPLATE_INVALID: 'invalid',
    TEMPLATE_DELETED: 'deleted',
}

# Host status
HOST_OK = 0
HOST_ERROR = 1
HOST_STATUS = {
    HOST_OK: 'ok',
    HOST_ERROR: 'error',
}

# Host Hypervisor Type
HOST_XEN = 0
HOST_KVM = 1
HOST_TYPE = {
    HOST_XEN: 'xen',
    HOST_KVM: 'kvm',
}


