from flask import g, request

from modules.logger import log
from modules.secrets import hosts, keyring, secrets
from modules.secure import encrypt, decrypt

def init_cookie_store():
    """Initializes the cookie store for use with the current response.
    """
    g.__existing_cookies__ = {}
    g.__cookies__ = {}

    for cookie in request.cookies.keys():
        g.__existing_cookies__[cookie] = request.cookies[cookie]

def get_cookie(cookie):
    """Returns the value of the request cookie.

    Args:
        cookie: The key of the cookie to get the value of.
    Returns:
        The value of the cookie named `cookie`. If `cookie`
        is a string set by set_cookie, then it will be encrypted.
        Luckily for you, get_cookie will decrypt it for you; a plain-text
        version of the cookie will be returned.

        In the event that a cookie is encrypted and cannot be decrypted
        None will be returned.
    """
    if cookie in g.__cookies__:
        val = g.__cookies__[cookie]['value']
    elif cookie in g.__existing_cookies__:
        val = g.__existing_cookies__[cookie]
    else:
        return None

    if len(val) > 5 and val[:5] == 'bkmk|':
        val = val[5:]

        try:
            val = decrypt(val, keyring.gatekeeper_key)
        except:
            log.error('Unable to decrypt bkmk encrypted cookie ({}): {}'.format(cookie, val))
            return False

    return val

def set_cookie(key, val, max_age=60*60*24*365, domain='.{}'.format(hosts.bookmark), secure=not secrets.DEBUG, httponly=True):
    """Sets a cookie.

    Cookies set by applications should always be HTTP only. In the event
    that some JavaScript needs to read a cookie, the backend may provide
    cookie values on an as-needed basis.

    Args:
        key (required): The key to use when naming the cookie.
        val (required): The value to use when setting the cookie.
        max_age (default=365 days):
            The max_age value of the cookie. Used to specify
            when the cookie should expire.
        domain (default=*.):
            The domain to bind the cookie to. By default, the cookie
            is bound to all domains and subdomains of Bookmark.
        secure (default=False if DEBUG else True):
            Whether the cookie should only be accessible through HTTPS.
        http_only (default=True):
            Whether the cookie should only be accessible by the server.
    """
    g.__cookies__[key] = {
        'key': key,
        'value': 'bkmk|' + encrypt(val, keyring.gatekeeper_key),
        'max_age': max_age,
        'domain': domain,
        'secure': secure,
        'httponly': httponly,
        'path': '/'
    }

def delete_cookie(key):
    """Deletes the specified cookie.

    This function just sets the cookie's max_age
    to be 0. If the cookie does not exist, this
    function does nothing.

    NOTE:
        If you are deleting an EXISTING cookie, it will
        not be deleted immediately.

        For example:
            Let cookie[x] = 0

            ```
            delete_cookie(x)
            y = get_cookie(x)
            ```

            Cookie x has been slated for deletion once
            a response is returned to the user. However,
            cookie x will still exist for the duration
            of the current request. In this example,
            y's value will be 0.

        An existing cookie is defined as one that was
        already set before the current request.

    Args:
        key: The key of the cookie to delete.
    """
    if key in g.__cookies__:
        del g.__cookies__[key]
    if key in g.__existing_cookies__:
        set_cookie(key, '', max_age=0)

def export_cookie_store(response):
    """Sends the appropriate reponse headers for each cookie in the store."""
    for key in g.__cookies__:
        response.set_cookie(**g.__cookies__[key])
