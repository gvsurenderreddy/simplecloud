# -*- coding: utf-8 -*-

from flask.ext.wtf import (HiddenField, SubmitField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, NumberRange
from flask.ext.wtf.html5 import IntegerField

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX)
        
from .models import Image
     
# Image Form    
class AddImageForm(Form):
    next = HiddenField()
    name = TextField(u'Choose the image name', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")
    src_path = TextField(u'Choose the image file path', [Required()],
            description=u"The image will be copied to IMAGEPOOL from this location.")

    submit = SubmitField('Save')

    def validate_name(self, field):
        if Image.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This image name is taken')

# Image not support edit 
'''
class EditImageForm(Form):
    next = HiddenField()
    name = TextField(u'Choose the image name', [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=u"Don't worry. you can change it later.")

    submit = SubmitField('Save')

    def validate_name(self, field):
        if Image.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(u'This image name is taken')
'''



