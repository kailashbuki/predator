#!/usr/bin/python2.6
# Copyright 2011 Kailash Budhathoki
# Author: kailash.buki@gmail.com


from gevent import monkey
monkey.patch_all()

from werkzeug.serving import run_simple
from app_creator import create_app

def main():
    '''runs the flask app
    '''
    app = create_app('etc.settings')[0]
    
    run_simple('0.0.0.0', 5000, app, True, True)

main()
