# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, TextField, AnyOf, Optional,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField)
from flask.ext.wtf import Required, Length, EqualTo, Email, NumberRange, URL
from flask.ext.wtf.html5 import EmailField, IntegerField
from flask.ext.login import current_user
from flaskext.babel import lazy_gettext as _
from ..user import User, USER_LOCALE_STRING
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX

class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    email = EmailField(_(u'Email'), [Required(), Email()])
    vm_quota = IntegerField(_(u'Quota of VirtualMachines'))
    locale_code = RadioField(_("Language"), [AnyOf([str(val) for val in USER_LOCALE_STRING.keys()])],
            choices=[(str(val), label) for val, label in USER_LOCALE_STRING.items()])

    submit = SubmitField(_(u'Save'))

    def validate_name(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_name(field.data):
            raise ValidationError(_("Please pick another name."))
    
    def validate_vm_quota(form, field):
        if (not current_user.is_admin()) and current_user.vm_quota != int(field.data):
            raise ValidationError(_("Only admin user can update vm quota."))

class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField(_('Current password'), [Required()])
    new_password = PasswordField(_('New password'), [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField(_('Password again'), [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(_(u'Save'))

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError(_("Password is wrong."))
