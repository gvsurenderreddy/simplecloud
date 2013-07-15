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
INACTIVE = 0
NEW = 1
ACTIVE = 2
USER_STATUS = {
    INACTIVE: 'inactive',
    NEW: 'new',
    ACTIVE: 'active',
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
