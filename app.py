import os

import redis

from flask import Flask, session
from flask_bcrypt import Bcrypt
from flask_kvsession import KVSessionExtension
from flask_wtf.csrf import CsrfProtect
from simplekv.decorator import PrefixDecorator
from simplekv.memory.redisstore import RedisStore

from modules.cookie import init_cookie_store, export_cookie_store
from modules.logger import log
from modules.secrets import hosts, secrets
from modules.util import static_url, persist_url

store = RedisStore(redis.StrictRedis(host=hosts.redis))
store = PrefixDecorator('gatekeeper_', store)

app = Flask('bookmark')

app.secret_key = secrets.gatekeeper_secret
app.server_name = hosts.gatekeeper
app.session_cookie_secure = True

bcrypt = Bcrypt(app)

KVSessionExtension(store, app)

# Variable injections that should be available to all templates.
@app.context_processor
def injections():
    to_inject = {
        'hosts': hosts,
        'signin_redirect': secrets.signin_redirect,
        'static_url': static_url,
        'persist_url': persist_url
    }

    # Create a dummy csrf function for templates if debug is on.
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
    # Sessions should be permanent.
    session.permanent = True
    # Initialize the local cookie store.
    init_cookie_store()

    log.info('Received request.')

@app.after_request
def post_request(response):
    # Export the local cookie store by
    # sending appropriate response headers.
    export_cookie_store(response)
    return response

from gatekeeper import *

if __name__ == '__main__':
    app.run(port=secrets.port, debug=secrets.DEBUG)
