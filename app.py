import os

from flask import Flask
from flask_bcrypt import Bcrypt

from models.account import Account
from modules.secrets import secrets

app = Flask('bookmark')

app.secret_key = secrets.gatekeeper_secret

bcrypt = Bcrypt(app)
