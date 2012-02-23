#!/usr/bin/env python


import werkzeug

from pymongo import Connection


DB = Connection()['predator']
# ensuring indexing in fingerprint collection
DB.fingerprint.create_index('fingerprint')
password = werkzeug.generate_password_hash('admin')
DB.user.save({'username': 'admin', 'fullname':'admin', 'password': password, \
                                                'email':' admin@predator.com'})

