# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, RadioField, DateField, 
        PasswordField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, Email, NumberRange
from flask.ext.wtf.html5 import EmailField, IntegerField

from ..user import USER_ROLE, USER_STATUS
from ..user import User
from .models import Task
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        NAME_LEN_MIN, NAME_LEN_MAX, VM_QUOTA_MIN, VM_QUOTA_MAX)

# User Form
class AddUserForm(Form):
    next = HiddenField()
    email = EmailField(u'Email', [Required(), Email()],
            description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    name = TextField(u'Choose your username', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    submit = SubmitField(u'Save')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')

class EditUserForm(Form):
    next = HiddenField()    
    name = TextField(u'User Name', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)])
    role_code = RadioField(u"Role", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_code = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    vm_quota = IntegerField(u"VM Quota", [Required(), NumberRange(VM_QUOTA_MIN, VM_QUOTA_MAX)])
    created_time = DateField(u'Created time')
    submit = SubmitField(u'Save')
    
    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')



