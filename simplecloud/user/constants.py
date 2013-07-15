# -*- coding: utf-8 -*-

# User role
ADMIN = 0
STAFF = 1
USER = 2
USER_ROLE = {
    ADMIN: 'admin',
    STAFF: 'staff',
    USER: 'user',
}

# User status
USER_INACTIVE = 0
USER_NEW = 1
USER_ACTIVE = 2
USER_DELETED = 3
USER_STATUS = {
    USER_INACTIVE: 'inactive',
    USER_NEW: 'new',
    USER_ACTIVE: 'active',
    USER_DELETED: 'deleted',
}


# VM status
VM_OK = 0
VM_INVALID = 1
VM_DELETED = 2
VM_STATUS = {
    VM_OK: 'ok',
    VM_INVALID: 'invalid',
    VM_DELETED: 'deleted',
}

STRING_LEN = 256
