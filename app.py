import os

from flask import Flask
from flask_bcrypt import Bcrypt

from models.account import Account
from modules.cookie import init_cookie_store, export_cookie_store
from modules.secrets import secrets

app = Flask('bookmark')

app.secret_key = secrets.gatekeeper_secret

bcrypt = Bcrypt(app)

@app.before_request
def pre_request():
    init_cookie_store()

@app.after_request
def post_request(response):
    export_cookie_store(response)
    return response