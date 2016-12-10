from flask import request

from modules.secrets import secrets

__existing_cookies__ = {}
__cookies__ = {}

def init_cookie_store():
    global __existing_cookies__

    for cookie in request.cookies.keys():
        __existing_cookies__[cookie] = request.cookies[cookie]

def get_cookie(cookie):
    global __existing_cookies__
    global __cookies__

    if cookie in __cookies__:
        return __cookies__[cookie]['value']
    elif cookie in __existing_cookies__:
        return __existing_cookies__[cookie]
    else:
        return None

# Cookies set by applications should always be HTTP only. In the event
# that some JavaScript needs to read a cookie, the backend may provide
# cookie values on an as-needed basis.
def set_cookie(key, val, max_age=60*60*24*365, domain='*.{}'.format(secrets.bookmark_host), secure=True, httponly=True):
    global __cookies__

    __cookies__[key] = {
        'key': key,
        'value': val,
        'max_age': max_age,
        'doamin': domain,
        'secure': secure,
        'httponly': httponly
    }

def export_cookie_store(response):
    global __cookies__

    for key in __cookies__.keys():
        response.set_cookie(**__cookies__[key])
