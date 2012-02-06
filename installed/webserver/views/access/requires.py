from functools import wraps
from flask import request, redirect, session, url_for

from models.documents import User

def login():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'username' not in session:
                return redirect(url_for('base.login', next=request.url))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            me = session.get('username')
            if me:
                if me == 'admin':
                    return f(*args, **kwargs)
                else:
                    return "Only allowed for admin"
            else:
                return redirect(url_for('base.login', next=request.url))
        return decorated_function
    return decorator