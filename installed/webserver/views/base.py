#!/usr/bin/env python
# Copyright 2011 Kailash Budhathoki
# Author: kailash.buki@gmail.com


import datetime
import os

from flask import Flask, Blueprint, request, session, redirect, render_template, url_for
from pymongo import Connection
import werkzeug

from contrib.log_handler import logger
from forms.forms import UserForm
from models.documents import User, Audit
from views.contrib.cookies import make_cookie, unserialize_cookie, \
                check_login_cookies, make_rememberme_cookie
from views.access import requires
from app_creator import app, connection

DB = Connection()[app.config['MONGODB_DATABASE']]
base = Blueprint('base', __name__)

@base.route('/', methods=['GET'])
def index():
    if session.get('username'): 
        return redirect(url_for('.dashboard'))

    return redirect(url_for('.login'))

@base.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    remember = False
    cookie_flag = False
    
    next_url = request.args.get('next')
    if next_url:
        response_body = redirect(next_url)
    else:
        response_body = redirect(url_for("base.dashboard"))
    response = app.make_response(response_body)
                    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember_me = request.form.get('remember_me')
        if username and password:
            me = User.find_one({'username':username})
            if me:
                hash_password = me.get('password', '')
                if werkzeug.check_password_hash(hash_password, password):
                    session['username'] = me['username'] 
                    if remember_me:
                        remember = True
                else:
                    error = 'Invalid password'
            else:
                error = 'Invalid username'
                logger.warning('Invalid username')
                return render_template('login.html', error=error)
        else:
            error = "username and password fields are required."
            logger.warning("username and password fields are required")
            return render_template('login.html', error=error)

    if not session.get('username'):
        username = check_login_cookies(request.cookies)
        if username:
            cookie_flag = True
            session['username'] = username 

    if session.get('username'):
        if remember or cookie_flag:
            response.set_cookie('TK', make_rememberme_cookie(), 2592000) # 30 days
        logger.info("login successful")
        return response
    else:
        return render_template('login.html', error=error)
        
def format_ts(obj):
    obj['ts'] = obj['_id'].generation_time.strftime("%d/%m/%Y %I:%M:%S")
    return obj

@base.route('/dashboard', methods=['GET'])
@requires.login()
def dashboard():
    page_number = request.args.get('page_number')
    if not page_number:
        page_number = 1
    
    page_number = int(page_number)
    if page_number < 1 :
        return 'Invalid.'
    
    uploaded = Audit.find({'username': session['username'], 'type': 'upload'}).count()
    checked = Audit.find({'username': session['username'], 'type': 'check'}).count()
    
    per_page = 15
    total_logs = Audit.find({'username': session['username']}).count()
    total_pages = total_logs / per_page
    if total_logs % per_page:
        total_pages += 1
    
    if total_pages > 1:
        show_pagination_link = True
    else:
        show_pagination_link = False
    
    audit_logs = []
    for log in Audit.find({'username': session['username']}).sort('_id', -1).skip(per_page * (page_number - 1)).limit(per_page):
        audit_logs.append(log)
    
    audit_logs = [format_ts(audit_log) for audit_log in audit_logs]
    return render_template('dashboard.html', audit_logs=audit_logs, \
                           uploaded=uploaded, checked=checked, \
                           page_number=page_number, total_pages=total_pages,\
                           show_pagination_link=show_pagination_link) 
    
@base.route('/logout', methods=['GET'])
def logout():
    me = session.pop('username', None)
    if me:
        response_body = redirect(url_for('base.login'))
        response = app.make_response(response_body)
        
        if request.cookies.get('TK'):
            cookie = unserialize_cookie(request.cookies['TK'])
            user = User.find_one({'username': me})
            if user and user['last_login'].get(cookie['token']):
                user['last_login'].pop(cookie['token'])
                user.save()
            response.delete_cookie('TK')
        return response
    return render_template('dashboard.html')

@base.route('/test', methods=['GET'])
def test():
    connection.drop_database(app.config['MONGODB_DATABASE'])
    # ensuring indexing in fingerprint collection
    DB.fingerprint.create_index('fingerprint')
    password1 = werkzeug.generate_password_hash('admin')
    user1 = User()
    user1.update({'username':'admin', 'fullname':'admin', 'password':password1, 'email':'makalu@admin.com'})
    user1.save()
    password2 = werkzeug.generate_password_hash('rick')
    user2 = User()
    user2.update({'username':'rick', 'fullname':'rick fowler', 'password':password2, 'email':'rick@immune.dk'})
    user2.save()
    return 'DB indexed and User admin added to the db.'

    
