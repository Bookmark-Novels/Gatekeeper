import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CsrfProtect

from models.account import Account
from modules.cookie import init_cookie_store, export_cookie_store
from modules.secrets import secrets

app = Flask('bookmark')

app.secret_key = secrets.gatekeeper_secret
app.server_name = secrets.gatekeeper_host
app.session_cookie_secure = True

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.context_processor
def injections():
    to_inject = {}
    
    if secrets.DEBUG:
        to_inject['csrf_token'] = lambda: 0

    return to_inject

# Enabling CSRF protection seems to break
# automatic reloads on template changes.
#
# Do not enable protection in dev environments.
if not secrets.DEBUG:
    CsrfProtect(app)

@app.before_request
def pre_request():
    init_cookie_store()

@app.after_request
def post_request(response):
    export_cookie_store(response)
    return response

from gatekeeper import *

if __name__ == '__main__':

    app.run(port=secrets.port, debug=secrets.DEBUG)