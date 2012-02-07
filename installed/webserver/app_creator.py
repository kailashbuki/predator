#!/usr/bin/env python
# Copyright 2011 Kailash Budhathoki
# Author: kailash.buki@gmail.com


from flask import Flask
from mongokit import Connection


def create_app(config_filename):
    '''Creates an app reading the config file
    '''
    global app, connection

    app = Flask(__name__)
    app.config.from_object(config_filename)

    connection = Connection(app.config['MONGODB_HOST'],
                            app.config['MONGODB_PORT'])
   
    from views.admin import admin
    from views.base import base
    from views.cop import cop
    
    app.register_blueprint(admin, url_prefix='/admin')
    app.register_blueprint(base)
    app.register_blueprint(cop, url_prefix='/cop')

    return app, connection

