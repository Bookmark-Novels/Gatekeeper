from cryptography.fernet import Fernet

from flask import request

def get_ip():
    if 'X-Forwarded-For' in request.headers:
        return '|'.join(request.headers.getlist('X-Forwarded-For'))

    return request.remote_addr

def encrypt(s):
    f = Fernet(k)
    return f.encrypt(s)

def decrypt(s):
    f = Fernet(k)
    return f.decrypt(s)