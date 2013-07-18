# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, NumberRange
from flask.ext.wtf.html5 import IntegerField
from flaskext.babel import lazy_gettext as _

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX,
        VCPU_NUM_MIN, VCPU_NUM_MAX, MEM_SIZE_MIN, MEM_SIZE_MAX, 
        DISK_SIZE_MIN, DISK_SIZE_MAX)

from .constants import TEMPLATE_OK        
from .models import Template
from ..image import Image 
     
# Template Form
class AddTemplateForm(Form):
    next = HiddenField()
    name = TextField(_(u'Choose the template name'), [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=_(u"Don't worry. you can change it later."))
    image_id = IntegerField(_(u'Choose the image attached on this template'), [Required()])
    vcpu_desc = _("Choose the VCPU number (From %(min)d to %(max)d)",  min=VCPU_NUM_MIN, max=VCPU_NUM_MAX)
    vcpu = IntegerField(vcpu_desc, [Required(), NumberRange(VCPU_NUM_MIN, VCPU_NUM_MAX)])
    memory_desc = _("Choose the memory size (From %(min)dM to %(max)dM)",  min=MEM_SIZE_MIN, max=MEM_SIZE_MAX)
    memory = IntegerField(memory_desc, [Required(), NumberRange(MEM_SIZE_MIN, MEM_SIZE_MAX)])
    disk_desc = _("Choose the disk size (From %(min)dM to %(max)dM)",  min=DISK_SIZE_MIN, max=DISK_SIZE_MAX)
    disk = IntegerField(disk_desc, [Required(), NumberRange(DISK_SIZE_MIN, DISK_SIZE_MAX)])

    submit = SubmitField(_('Save'))

    def validate_name(self, field):
        if Template.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_(u'This template name is taken'))
            
    def validate_image_id(self, field):
        if Image.query.filter_by(id=field.data).first() is None:
            raise ValidationError(_(u'This Image is not found'))

# Template not support edit
# class EditTemplateForm(Form)

# TODO: BAD Design!!! just for implementing the create vm dialog in Templates page (user view)
class AddVMForm(Form):
    next = HiddenField()
    name = TextField(_(u'Choose virtualmachine name'), [Required(), Length(1, NAME_LEN_MAX)])
    template_id = IntegerField(_(u'Choose the template ID'), [Required()])
    
    submit = SubmitField('Save')
            
    def validate_template_id(self, field):
        template = Template.query.filter_by(id=field.data).first()
        if template is None:
            raise ValidationError(_(u'This Template is not found'))
        if template.status_code != TEMPLATE_OK:
            raise ValidationError(_(u'This Template is not OK'))
