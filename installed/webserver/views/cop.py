#!/usr/bin/env python
# Copyright 2011 Kailash Budhathoki
# Author: kailash.buki@gmail.com

import gevent
import json
import logging
import re
import werkzeug

from flask import Flask, flash, jsonify, Blueprint, request, session, redirect, \
                    render_template, url_for

from contrib.calling import agent_req_dispatcher
from contrib.validating import is_valid_file
from access import requires
from models.documents import User, Audit
from app_creator import app


cop = Blueprint('cop', __name__)
filepat = re.compile('\d/(.*)')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 #50MB max upload size


def get_user_prefs():
    """
    """
    label_scale = [None for i in range(100)]
    user = User.find_one({'username': session['username']})
    labels = user['labels']
    threshold = user['threshold']
    
    for label, value in labels.iteritems():
        ran, color = value
        start, end = ran.split('-')
        
        intermediate_values = range(int(start) + 1, int(end) + 1)
        for i in intermediate_values:
            label_scale[i-1] = label
            
    return labels, label_scale, threshold
   
def filter_row(row, labels, label_scale, threshold):
    """
    """
    label = color = ''
    above_threshold = False
    match_percentage = row[1]
    trimmed_filename = filepat.findall(row[0])[0]
    row[0] = trimmed_filename
    
    if match_percentage >= threshold:
        label = label_scale[int(match_percentage) - 1]
        if label:
            color = labels[label][1]
        above_threshold = True
    
    row.append(label)
    row.append(color)
    
    return above_threshold, row
    
@cop.route('/check', methods = ['GET', 'POST'])
@requires.login()
def check():
    result = None
    if request.method == 'POST':
        try:
            uploaded = request.files.get('file')
            error = """<div id="match" style="display:none;"></div>
                        <div class="alert-message error fade in">
                        <a class="close" href="#">x</a>
                        <p>"""
            if not uploaded:
                return error + "File not supplied." + "</p></div>"
                
            filename = uploaded.filename
            if not is_valid_file(filename):
                return error + "Not a valid file type. Please use file in pdf format." \
                                + "</p></div>"
                
            audit = Audit()
            audit.update(dict(
                        username = session['username'],
                        type = 'check',
                        doc = filename))
            audit.save()
                
            filepath = '/tmp/%s' % filename
            content = uploaded.read()
            with open(filepath, 'w') as stream:
                stream.write(content)
            
    
            s = agent_req_dispatcher()
            content = '<div id="match" style="display:none;"></div>'
    
            s.send_json(dict(pdf_path = filepath, do_what = 'check'))
            response = s.recv_multipart()
            result = json.loads(response[0])
            logging.warn('Webserver: received result; result=%s' % result)
        
            if result['match']['per_match']:
                labels, label_scale, threshold = get_user_prefs()
                stat = label_scale[int(result['match']['total_match']) - 1]
                
                content += """<div class="match_overview"><span class="desc"
                            style="margin-right: 15px;">
                            Results </span><span class="group">
                            <span class="match_percentage">
                            <span class="key">Percentage Match =</span>
                            <strong>%d</strong> %%</span><span class="divider">|
                            </span><span class="match_documents"><span class="key">
                            Matching Documents = </span><strong>%d</strong>
                            <span class="divider">|</span><span class="match_label">
                            <span class="key">Label =</span>
                            <strong>%s</strong></span></span></div>
                            <table class='zebra-striped bordered-table'>
                            <thead><tr><th>#</th><th>File
                            </th><th>Match</th></tr>
                            </thead><tbody>""" % (result['match']['total_match'], \
                                            len(result['match']['per_match']), stat)
                for i, row in enumerate(result['match']['per_match']):
                    above_threshold, row = filter_row(row, labels, label_scale, threshold)
                    if above_threshold:
                        content += """<tr><td>%s</td><td>%s<span style='background: #%s;
                                    color: #FFF; border-radius: 2px; margin-left: 60px;
                                    padding: 2px 6px 2px 6px;'>%s</span></td>
                                    <td>%d %%</td></tr>""" % (i+1, row[0], row[3], row[2], row[1])
                            
                content += '</tbody></table>'
            else:
                content += """<div class="alert-message success fade in">
                            <a class="close" href="#">x</a>
                            <p>No match found.</p></div>
                            """
            
            return content
        
        except werkzeug.exceptions.RequestEntityTooLarge, e:
            logger.warn('Maximum file size exceeded while uploading file')
            flash('File size exceeded the maximum upload limit(50MB).')
    
    return render_template('file_check.html', result=result)

@cop.route('/result')
@requires.login()
def result():
    #TODO: get result of the detection here
    return 'result'

@cop.route('/get_copy')
@requires.login()
def show_copy():
    #TODO: show the copied part in the document
    return 'match'