from cryptography.fernet import Fernet

from flask import request

def get_ip():
    if 'X-Forwarded-For' in request.headers:
        return '|'.join(request.headers.getlist('X-Forwarded-For'))

    return request.remote_addr

def encrypt(s, k):
    f = Fernet(str(k).encode('utf-8'))

    # Ensure this is actually a string which
    # is then promptly turned into a bytes object.
    s = str(s).encode('utf-8')
    # Fernet#encrypt returns a bytes object.
    return str(f.encrypt(s), 'utf-8')

def decrypt(s, k):
    f = Fernet(str(k).encode('utf-8'))
    # Fernet#decrypt returns a bytes object.
    return str(f.decrypt(s.encode('utf-8')), 'utf-8')
