# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, NumberRange
from flask.ext.wtf.html5 import IntegerField

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX,
        VCPU_NUM_MIN, VCPU_NUM_MAX, MEM_SIZE_MIN, MEM_SIZE_MAX, 
        DISK_SIZE_MIN, DISK_SIZE_MAX)

from .constants import TEMPLATE_OK        
from .models import Template
from ..image import Image 
     
# Template Form
class AddTemplateForm(Form):
    next = HiddenField()
    name = TextField(u'Choose the template name', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    image_id = IntegerField(u'Choose the image attached on this template', [Required()])
    vcpu_desc = "Choose the VCPU number (From " + str(VCPU_NUM_MIN) + " to " + str(VCPU_NUM_MAX) +")"
    vcpu = IntegerField(unicode(vcpu_desc), [Required(), NumberRange(VCPU_NUM_MIN, VCPU_NUM_MAX)])
    memory_desc = "Choose the Memory size (From " + str(MEM_SIZE_MIN) + "M to " + str(MEM_SIZE_MAX) +"M)"
    memory = IntegerField(unicode(memory_desc), [Required(), NumberRange(MEM_SIZE_MIN, MEM_SIZE_MAX)])
    disk_desc = "Choose the Disk size (From " + str(DISK_SIZE_MIN) + "M to " + str(DISK_SIZE_MAX) +"M)"
    disk = IntegerField(unicode(disk_desc), [Required(), NumberRange(DISK_SIZE_MIN, DISK_SIZE_MAX)])

    submit = SubmitField('Save')

    def validate_name(self, field):
        if Template.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This template name is taken')
            
    def validate_image_id(self, field):
        if Image.query.filter_by(id=field.data).first() is None:
            raise ValidationError(u'This Image is not found')

# Template not support edit
# class EditTemplateForm(Form)

# TODO: BAD Design!!! just for implementing the create vm dialog in Templates page (user view)
class AddVMForm(Form):
    next = HiddenField()
    name = TextField(u'Choose virtualmachine name', [Required(), Length(1, NAME_LEN_MAX)],
            description=u"virtualmachine name.")
    template_id = IntegerField(u'Choose the template ID', [Required()])
    
    submit = SubmitField('Save')
            
    def validate_template_id(self, field):
        template = Template.query.filter_by(id=field.data).first()
        if template is None:
            raise ValidationError(u'This Template is not found')
        if template.status_code != TEMPLATE_OK:
            raise ValidationError(u'This Template is not OK')
