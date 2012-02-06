#!/usr/bin/python2.6
# Copyright 2011 Kailash Budhathoki
# Author: kailash.buki@gmail.com


import datetime
import os

from flask import session
from werkzeug.contrib.securecookie import SecureCookie

from models.documents import User
from app_creator import app


secret_key = app.config['SECRET_KEY']

def make_cookie(**kwargs):
    return SecureCookie(kwargs, secret_key).serialize()

def unserialize_cookie(cookie):
    return SecureCookie.unserialize(cookie, secret_key)

def make_session_cookie(username):
    token = os.urandom(16).encode('hex')
    cookie = make_cookie(username=username, token=token)
    return cookie

def check_session_cookie(cookie):
    try:
        if not cookie.get('SK'):
            return
        cookie_data = unserialize_cookie(cookie['SK'])
        username = cookie_data['username']
        return username
    except Exception:
        return

def make_rememberme_cookie():
    username = session['username'] # search for username key in custom cookie
    token = os.urandom(16).encode('hex')
    cookie = make_cookie(username=username, token=token)
    
    user = User.find_one({'username': username})
    user['last_login'][token] = datetime.datetime.now()
    user.save()

    return cookie

def check_login_cookies(cookie):
    if not cookie.get('TK'):
        return

    username_random = unserialize_cookie(cookie['TK'])
    username = username_random['username']
    token = username_random['token']

    user = User.find_one({'username': username})

    if user['last_login'].get(token):
        if (user['last_login'].get(token) + datetime.timedelta(days=30)) <  datetime.datetime.now():
            return
        user['last_login'].pop(token, None)
        user.save()
        return username
    return