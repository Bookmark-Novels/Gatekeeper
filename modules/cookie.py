from flask import request

from modules.secrets import secrets

__cookies__ = None

def init_cookie_store():
    global __cookies__

    __cookies__ = request.cookies

def get_cookie(cookie):
    global __cookies__

    if cookie in __cookies__:
        return __cookies__[cookie]
    else:
        return None

def set_cookie(key, val):
    global __cookies__

    __cookies__[key] = val

def export_cookie_store(response):
    global __cookies__

    for key in __cookies__.keys():
        response.set_cookie(
            key,
            value=__cookies__[key],
            max_age=60*60*24*365,
            domain='*.{}'.format(secrets.bookmark_host)
        )
