# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, RadioField, DateField, 
        PasswordField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, Email
from flask.ext.wtf.html5 import EmailField

from ..user import USER_ROLE, USER_STATUS
from ..user import User
from ..utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX)

class AddVMForm(Form):
    next = HiddenField()
    name = TextField(u'Choose virtualmachine name', [Required(), Length(VMNAME_LEN_MIN, VMNAME_LEN_MAX)],
            description=u"virtualmachine name.")
    email = EmailField(u'Email', [Required(), Email()],
            description=u"What's your email address?")
    password = PasswordField(u'Password', [Required(), Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
            description=u'%s characters or more! Be tricky.' % PASSWORD_LEN_MIN)
    name = TextField(u'Choose your username', [Required(), Length(USERNAME_LEN_MIN, USERNAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    submit = SubmitField('Save')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This username is taken')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(u'This email is taken')
