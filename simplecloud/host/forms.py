# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField, RadioField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, NumberRange
from flask.ext.wtf.html5 import IntegerField

from flaskext.babel import lazy_gettext as _

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX)
from .constants import HOST_TYPE, HOST_KVM
from .models import Host
     

# Host Form    
class AddHostForm(Form):
    next = HiddenField()
    address = TextField(_(u'The IP address or hostname of target host'), [Required()])
    type_code = RadioField(_(u"Hypervisor Type"), [AnyOf([str(val) for val in HOST_TYPE.keys()])],
            choices=[(str(val), label) for val, label in HOST_TYPE.items()], default=HOST_KVM)
    
    username = TextField(_(u'The Username used by libvirt+ssh connection'), [Required()], default="simplecloud")

    submit = SubmitField(_(u'Save'))

    def validate_address(self, field):
        if Host.query.filter_by(address=field.data).first() is not None:
            raise ValidationError(_(u'This host is added'))

class EditHostForm(Form):
    next = HiddenField()
    type_code = RadioField(_(u"Hypervisor Type"), [AnyOf([str(val) for val in HOST_TYPE.keys()])],
            choices=[(str(val), label) for val, label in HOST_TYPE.items()])
    username = TextField(_(u'The Username used by libvirt+ssh connection'), [Required()])
    submit = SubmitField(_(u'Save'))
    def validate_address(self, field):
        if Host.query.filter_by(address=field.data).first() is not None:
            raise ValidationError(_(u'This host is added'))



