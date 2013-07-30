# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, RadioField, DateField, 
        PasswordField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, Email, NumberRange
from flask.ext.wtf.html5 import EmailField, IntegerField

from flaskext.babel import lazy_gettext as _
from ..user import USER_ROLE, USER_STATUS
from ..user import User
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        NAME_LEN_MIN, NAME_LEN_MAX, VM_QUOTA_MIN, VM_QUOTA_MAX)

# User Form
class AddUserForm(Form):
    next = HiddenField()
    name = TextField(_(u'Choose your username'), [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=_(u"Don't worry. you can change it later."))
    email = EmailField(_(u'Email'), [Required(), Email()],
            description = _(u"What's your email address?"))
    password = PasswordField(_(u'Password'), [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=_('%(number)d characters or more! Be tricky.', number=PASSWORD_LEN_MIN))
    vm_quota = IntegerField(_(u'Quota of VirtualMachines'), default=2)
    submit = SubmitField(_(u'Save'))

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_(u'This username is taken'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_(u'This email is taken'))

class EditUserForm(Form):
    next = HiddenField()
    role_code = RadioField(_("Role"), [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_code = RadioField(_("Status"), [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    vm_quota = IntegerField(_("VM Quota"), [Required(), NumberRange(VM_QUOTA_MIN, VM_QUOTA_MAX)])
    created_time = DateField(_('Created time'))
    submit = SubmitField(_('Save'))
    
    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_(u'This username is taken'))



