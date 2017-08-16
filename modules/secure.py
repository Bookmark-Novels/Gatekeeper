from flask import request

from .common import locksmith

def get_ip():
    """Attempts to return a user's IP address.

    Returns:
        The user's IP address. This may return 127.0.0.1 if
        the web server is not configured to properly forward addresses.
    """
    if 'X-Forwarded-For' in request.headers:
        return '|'.join(request.headers.getlist('X-Forwarded-For'))

    return request.remote_addr

def get_request_info():
    return {
        "ip": get_ip(),
        "request_path": request.full_path,
        "request_method": request.method,
        "request_scheme": request.scheme,
        "request_post": request.form,
        "request_args": request.args,
        "request_cookies": request.cookies,
        "request_headers": str(request.headers).strip(),
        "request_url": request.url,
        "request_endpoint": request.endpoint
    }

def encrypt(s):
    """Returns an encrypted version of a string.

    Args:
        s: The string to encrypt.
    Returns:
        An encrypted version of `s`.
    """
    return locksmith.encrypt(s)

def decrypt(s):
    """Returns a decrypted version of a string.

    Args:
        s: The string to decrypt.
    Returns:
        A decrypted plain-text version of `s`.
    """
    return locksmith.decrypt(s)
