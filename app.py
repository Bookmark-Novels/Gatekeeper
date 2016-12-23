import os

import redis

from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_kvsession import KVSessionExtension
from flask_wtf.csrf import CsrfProtect
from simplekv.decorator import PrefixDecorator
from simplekv.memory.redisstore import RedisStore

from models.account import Account
from modules.cookie import init_cookie_store, export_cookie_store
from modules.secrets import hosts, secrets

store = RedisStore(redis.StrictRedis(host=hosts.redis))
store = PrefixDecorator('gatekeeper_', store)

app = Flask('bookmark')

app.secret_key = secrets.gatekeeper_secret
app.server_name = hosts.gatekeeper
app.session_cookie_secure = True

bcrypt = Bcrypt(app)

KVSessionExtension(store, app)

@app.context_processor
def injections():
    to_inject = {
        'hosts': hosts,
        'signin_redirect': secrets.signin_redirect
    }

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
    session.permanent = True
    init_cookie_store()

@app.after_request
def post_request(response):
    export_cookie_store(response)
    return response

from gatekeeper import *

if __name__ == '__main__':
    app.run(port=secrets.port, debug=secrets.DEBUG)
