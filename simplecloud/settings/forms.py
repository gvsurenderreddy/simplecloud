# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import (HiddenField, TextField, AnyOf, Optional,
        PasswordField, SubmitField, TextAreaField, IntegerField, RadioField,
        FileField, DecimalField)
from flask.ext.wtf import Required, Length, EqualTo, Email, NumberRange, URL
from flask.ext.wtf.html5 import URLField, EmailField, TelField
from flask.ext.login import current_user

from ..user import User
from ..utils import PASSWORD_LEN_MIN, PASSWORD_LEN_MAX

class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()])
    vm_quota = DecimalField(u'Quota of VirtualMachines', [Required()])
    submit = SubmitField(u'Save')

    def validate_name(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_name(field.data):
            raise ValidationError("Please pick another name.")

class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField('Current password', [Required()])
    new_password = PasswordField('New password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField('Password again', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(u'Save')

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError("Password is wrong.")
