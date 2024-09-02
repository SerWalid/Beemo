from functools import wraps
from flask import redirect, url_for, session, redirect
from datetime import datetime, timedelta


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def pin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('parent_zone_pin') != '1234':
            return redirect(url_for('main.show_pin_modal'))
        return f(*args, **kwargs)
    return decorated_function

def logged_in_restricted(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:  # or any other condition to check if the user is logged in
            return redirect(url_for('main.Home'))  # redirect to a different page or show an error
        return f(*args, **kwargs)
    return decorated_function