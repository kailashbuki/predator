#!/usr/bin/env python
'''
forms used for validation in backend
'''

from wtforms import Form, TextField, PasswordField, TextAreaField,\
                        validators, ValidationError, SelectField

def validate_int(form, field):
    if not field.data.isdigit():
        raise ValidationError("That's not an integer")

def validate_label(form, field):
    for label, range_color in field.data.iteritems():
        if not label.isalnum():
            raise ValidationError("Label name %s is not alphanumeric." % label)
        
        range, color = range_color
        range_items = range.split('-')
        if not len(range_items):
            raise ValidationError("Range %s is invalid." % range)
            
        if not range_items[0].isdigit() and not range_items[1].isdigit():
            raise ValidationError("Range %s is invalid." %  range)
            
        if len(color) != 6:
            raise ValidationError("Color value %s is invalid." % color)

class UserForm(Form):
    '''form definition for user form
    '''
    username = TextField('Username', [validators.Length(min=3, max=50),\
                                      validators.Required()])
    password = PasswordField('Password', [
        validators.EqualTo('confirm_password', message='Passwords must match'),
        validators.Required(),
        validators.Length(min=5, max=50)
    ])
    confirm_password = PasswordField('Re-enter password')
    fullname = TextField('Full name', [validators.Length(min=2, max=50),\
                                       validators.Required()])
    email = TextField('Email', \
                [validators.Email(message="Doesn't look like a valid email"),
                    validators.Required()
                ])
    threshold = TextField('Threshold', [validate_int])