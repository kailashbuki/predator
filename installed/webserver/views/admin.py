#!/usr/bin/env python
# Copyright 2011 Kailash Budhathoki
# Author: kailash.buki@gmail.com

import subprocess

from flask import Flask, Blueprint, request, session, redirect, render_template,\
                    url_for, flash
import werkzeug

from contrib.log_handler import logger
from contrib.calling import agent_req_dispatcher
from forms.forms import UserForm
from models.documents import User, Audit
from contrib.cookies import make_cookie, unserialize_cookie, \
                check_login_cookies, make_rememberme_cookie
from contrib.validating import is_valid_file
from access import requires

admin = Blueprint('admin', __name__)

@admin.route('/users', methods=['GET'])
@requires.admin()
def users_display():
    users = User.find()
    return render_template('display_users.html', users=users)

@admin.route('/users/create', methods=['GET', 'POST'])
@requires.admin()
def user_create():
    error = None
    form = UserForm(request.form)
    if request.method == 'POST' and form.validate(skip=['threshold']):
        username = request.form.get('username')
        password = werkzeug.generate_password_hash(request.form.get('password'))
        email = request.form.get('email')
        fullname = request.form.get('fullname')
        
        user = User.find_one({'username':username})
        if user:
            error = 'User %s already exists' % username
        else:
            user = User()
            user.update({'username':username, 'password':password, \
                         'email':email, 'fullname':fullname})
            user.validate()
            if user.validation_errors:
                error = str([k for k in user.validation_errors]) + \
                ' fields not valid'
            else:
                user.save()
                flash('User %s created.' % username, 'success')
                return redirect(url_for('.users_display'))
    flash(error, 'error')
    return render_template('create_user.html', form=form)
    
@admin.route('/users/edit/<username>', methods=['GET', 'POST'])
@requires.login()
def user_edit(username):
    threshold = range(99)
    if request.method == 'POST':
        username = request.form.get('username')
      
    if not username:
        return "Invalid action"
    
    user = User.find_one({'username':username})
    if not user:
        return 'User does not exist'
    if session['username'] != 'admin' and username != session['username']:
        return 'You are not allowed to perform that action'
    
    form = UserForm(request.form)
    skip = request.form.get('skip')

    if request.method == 'POST' and form.validate(skip=skip):
        if request.form.get('password'):
            if session['username']  != 'admin':
                previous_password = request.form.get('previous_password')
                if previous_password:
                    if werkzeug.check_password_hash(user['password'], previous_password):
                        pass
                else:
                    return render_template('edit_user.html', form=form, user=user)
            user['password'] = werkzeug.generate_password_hash(request.form.get('password'))    
        elif request.form.get('email') and request.form.get('fullname'):
            user['email'] = request.form.get('email')
            user['fullname'] = request.form.get('fullname')
        elif request.form.get('copy_labels'):
            user['labels'] = eval(request.form.get('copy_labels'))
        elif request.form.get('threshold'):
            user['threshold'] = int(request.form.get('threshold'))

        if user.validation_errors:
            return str([k for k in user.validation_errors]) + ' fields not valid'
        user.save()
        flash('Information updated for user %s.' % username, 'success')
    
    return render_template('edit_user.html', form=form, user=user, threshold=threshold)

@admin.route('/users/delete/<username>', methods=['GET'])
@requires.admin()
def user_delete(username):
    if username == 'admin':
        return 'admin cannot be deleted'
    user = User.find_one({'username':username})
    user.delete()
    flash('User %s deleted.' % username, 'success');
    return redirect(url_for('admin.users_display'))

@admin.route('/files', methods=['GET'])
@requires.admin()
def files_show():
    return 'files'

@admin.route('/files/upload', methods=['GET', 'POST'])
@requires.login()
def file_upload():
    error = None
    success = None
    if request.method == 'POST':
        uploaded = request.files['file']
        if not uploaded:
            flash('file not supplied', 'error')
            return render_template('file_upload.html', error=error)
            
        invalid = ''
        processed = ''
        for item in request.files.listvalues():
            for fileobj in item:
                filename = fileobj.filename
                if not is_valid_file(filename):
                    invalid += filename + ', '
                    continue
                
                audit = Audit()
                audit.update(dict(
                            username = session['username'],
                            type = 'upload',
                            doc = filename))
                audit.save()
                
                filepath = '/tmp/queue/%s' % filename
                content = fileobj.read()
                with open(filepath, 'w') as stream:
                    stream.write(content)
                
                s = agent_req_dispatcher()
                s.send_json(dict(pdf_path = filepath, do_what = 'archive'))
                processed += filename + ', '
        
        if invalid:
            invalid = invalid.rstrip(', ')
            flash('Invalid: { %s }' % invalid, 'error')
        if processed:
            processed = processed.rstrip(', ')
            flash('Processing : { %s }' % processed, 'info')
            
    return render_template('file_upload.html', error=error)
