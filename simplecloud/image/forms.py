# -*- coding: utf-8 -*-

from os.path import isfile

from flask.ext.wtf import (HiddenField, SubmitField, TextField)
from flask.ext.wtf import AnyOf
from flask.ext.wtf import Form, ValidationError
from flask.ext.wtf import Required, Length, EqualTo, NumberRange
from flask.ext.wtf.html5 import IntegerField
from flaskext.babel import lazy_gettext as _

from ..utils import (NAME_LEN_MIN, NAME_LEN_MAX)
from .constants import PATH_STRING_LEN        
from .models import Image
     
# Image Form    
class AddImageForm(Form):
    next = HiddenField()
    name = TextField(_(u'Choose the image name'), [Required(), Length(NAME_LEN_MIN, NAME_LEN_MAX)],
            description=_(u"Don't worry. you can change it later."))
    src_path = TextField(_(u'Choose the image file path'), [Required(), Length(1, PATH_STRING_LEN)],
            description=_(u"The image will be copied to IMAGEPOOL from this location."))

    submit = SubmitField(_('Save'))

    def validate_name(self, field):
        if Image.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_(u'This image name is taken'))
    
    def validate_src_path(self, field):
        if not isfile(field.data):
            raise ValidationError(_(u'The source file does not exist.'))

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



