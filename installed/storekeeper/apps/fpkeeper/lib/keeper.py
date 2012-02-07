#!/usr/bin/env python
#
# Copyright (C) 2011 by kailash.buki@gmail.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""library to store the fingeprints along with the document info into the DB
"""

__authors__ = [
    '"Kailash Budhathoki" <kailash.buki@gmail.com>'
]


import datetime
import errno
import os
import shutil

from pymongo import Connection


STORAGE_DIR = '%s/volumes/predator/files/' % os.environ['PREDATOR_HOME']


def _create_db_handler():
    """Creates a pymongo db handler
    
    Args: None
    
    Returns: None
    """
    connection = Connection()
    return connection['predator']

def _prepare_path(path):
    """ensures the parent directories for the given path

    Args: 
        path: Absolute path of the destination

    Returns: 
        None

    Raises: IOError
    """
    head, tail = os.path.split(path)
    if len(head) == 0:
        return 
    try:
        os.makedirs(head)
    except OSError, e:
        if e.errno != errno.EEXIST:
            raise

def _extract_filename(path):
    """Extracts the file name from the file path
        
    Args:
        path: Absolute file path
    
    Returns:
        filename 
    """
    head, tail = os.path.split(path)
    if len(head) == 0:
        return
    return tail

def archive_text_file(text_path):
    """Copies the text file from the temporary location to the archive path
    
    Args:
        text_path: The absolute path of the temporary location of the text file
    
    Returns: The relative path of the archived file. For example: '20110112/linux.txt'
    """
    today = datetime.date.today()
    dirname = datetime.datetime.strftime(today, '%Y%m%d')
    src, dst = text_path, STORAGE_DIR + dirname + '/'
    _prepare_path(dst)
    
    try:
        shutil.move(src, dst)
    except IOError, e:
        src_renamed = src + '_copy'
        os.rename(src, src_renamed)
        src = src_renamed
        shutil.move(src_renamed, dst)
    except:
        # catches other errors like "raise Error, "Destination path '%s' already exists" % real_dst"
        pass
    
    filename = _extract_filename(src)
    relative_path = dirname + '/' + filename
    
    return relative_path

def save_fp(fingerprint, doc_info):
    """Saves the fingerprints along with the document information in the db
    
    Args:
        doc_info: document information
        
    Returns: None
    """
    db = _create_db_handler()
    fingerprint_in_db = db.fingerprint.find_one({'fingerprint': fingerprint})
    
    if fingerprint_in_db:
        dinfo = fingerprint_in_db['doc_info']
        dinfo.append(doc_info)
        db.fingerprint.save(dict(fingerprint = fingerprint, doc_info = dinfo))
    else:
        db.fingerprint.save({
            'fingerprint': fingerprint,
            'doc_info': [doc_info]})

if __name__ == '__main__':
    archive_text_file('/Users/sagardh/Documents/Kernighan_Ritchie_Language_C.txt')
