# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo
from flask.ext.wtf.html5 import IntegerField

from ..utils import NAME_LEN_MIN, NAME_LEN_MAX
from ..template import Template, TEMPLATE_OK

class AddVMForm(Form):
    next = HiddenField()
    name = TextField(u'Choose virtualmachine name', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=u"virtualmachine name.")
    template_id = IntegerField(u'Choose the template ID', [Required()])
    
    submit = SubmitField('Save')
            
    def validate_template_id(self, field):
        template = Template.query.filter_by(id=field.data).first()
        if template is None:
            raise ValidationError(u'This Template is not found')
        if template.status_code != TEMPLATE_OK:
            raise ValidationError(u'This Template is not OK')

