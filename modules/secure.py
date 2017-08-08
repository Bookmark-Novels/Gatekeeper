from cryptography.fernet import Fernet

from flask import request

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
        "request_headers": request.headers,
        "request_url": request.url,
        "request_endpoint": request.endpoint
    }

def encrypt(s, k):
    """Returns an encrypted version of a string.

    Args:
        s: The string to encrypt.
        k: A 128-bit secret used to encrypt `s`. This should be a string.
    Returns:
        An encrypted version of `s`.
    """
    f = Fernet(str(k).encode('utf-8'))

    # Ensure this is actually a string which
    # is then promptly turned into a bytes object.
    s = str(s).encode('utf-8')
    # Fernet#encrypt returns a bytes object.
    return str(f.encrypt(s), 'utf-8')

def decrypt(s, k):
    """Returns a decrypted version of a string.

    Args:
        s: The string to decrypt.
        k: A 128-bit secret used to decrypt `s`. This should be a string.
    Returns:
        A decrypted plain-text version of `s`.
    Raises:
        cryptography.fernet.InvalidToken:
            If `s` is invalid in any way.
            Refer to https://cryptography.io/en/latest/fernet/ for further details.
    """
    f = Fernet(str(k).encode('utf-8'))
    # Fernet#decrypt returns a bytes object.
    return str(f.decrypt(s.encode('utf-8')), 'utf-8')
