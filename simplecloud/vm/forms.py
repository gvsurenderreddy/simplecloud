# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField, SelectField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo
from flask.ext.wtf.html5 import IntegerField
from flaskext.babel import lazy_gettext as _

from ..utils import NAME_LEN_MIN, NAME_LEN_MAX

class AddVMForm(Form):
    next = HiddenField()
    name = TextField(_(u'Choose virtualmachine name'), [Required(), Length(1, NAME_LEN_MAX)])
    template_id = SelectField(_(u'Choose the template'), choices=[])
    submit = SubmitField(_('Save'))
            
    #def validate_template_id(self, field):
    #    template = Template.query.filter_by(id=field.data).first()
    #    if template is None:
    #        raise ValidationError(_(u'This Template is not found'))
    #    if template.status_code != TEMPLATE_OK:
    #        raise ValidationError(_(u'This Template is not OK'))

