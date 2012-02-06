#!/usr/bin/env python
import datetime
import re

from mongokit import Document

from app_creator import app, connection

Document.authorized_types.append(basestring)

def email_validator(value):
   email = re.compile(r"(?:^|\s)[-a-z0-9_.]+@(?:[-a-z0-9]+\.)+[a-z]{2,6}(?:\s|$)",re.IGNORECASE)
   return bool(email.match(value))

def min_length(length):
   def validate(value):
      if len(value) >= length:
         return True
      return False
   return validate

@connection.register
class User(Document):
   structure = {
      'username': basestring,
      'email': basestring,
      'password': basestring,
      'fullname': basestring,
      'labels': dict,
      'threshold': int,
      'last_login': dict
   }
   required_fields = ['username', 'email', 'password']
   default_values = {'threshold': 5, 'labels': {}}
   validators = {
      'username': min_length(1),
      'email': email_validator
   }
   raise_validation_errors = False
   use_dot_notation = True
   
@connection.register
class Audit(Document):
   structure = {
      'username': basestring,
      'type': basestring,
      'doc': basestring
   }
   required_fields = ['username', 'type', 'doc']
   use_dot_notation = True
   
db = connection[app.config['MONGODB_DATABASE']]
for class_ in connection._registered_documents:
    globals()[class_] = getattr(getattr(db, class_.lower()), class_)