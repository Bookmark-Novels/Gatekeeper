from flask import g, request

from modules.secrets import hosts, keyring, secrets
from modules.secure import encrypt, decrypt

def init_cookie_store():
    g.__existing_cookies__ = {}
    g.__cookies__ = {}

    for cookie in request.cookies.keys():
        g.__existing_cookies__[cookie] = request.cookies[cookie]

def get_cookie(cookie):
    print(g.__cookies__)
    print(g.__existing_cookies__)

    if cookie in g.__cookies__:
        val = g.__cookies__[cookie]['value']
    elif cookie in g.__existing_cookies__:
        val = g.__existing_cookies__[cookie]
    else:
        return None

    if val[:5] == 'bkmk|':
        val = val[5:]
        val = decrypt(val, keyring.gatekeeper_key)

    return val

# Cookies set by applications should always be HTTP only. In the event
# that some JavaScript needs to read a cookie, the backend may provide
# cookie values on an as-needed basis.
#
# Set cookies to not be secure in development environments.
def set_cookie(key, val, max_age=60*60*24*365, domain='.{}'.format(hosts.bookmark), secure=not secrets.DEBUG, httponly=True):
    g.__cookies__[key] = {
        'key': key,
        'value': 'bkmk|' + encrypt(val, keyring.gatekeeper_key),
        'max_age': max_age,
        'domain': domain,
        'secure': secure,
        'httponly': httponly,
        'path': '/'
    }

    print(domain)

def delete_cookie(key):
    set_cookie(key, '', max_age=0)

def export_cookie_store(response):
    for key in g.__cookies__.keys():
        response.set_cookie(**g.__cookies__[key])
