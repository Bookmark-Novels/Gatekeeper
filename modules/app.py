from flask import Flask, session
from flask_kvsession import KVSessionExtension
from flask_wtf.csrf import CsrfProtect

from .common import config, redis_store
from .util import static_url, persist_url

app = Flask('bookmark')

app.secret_key = config.get_string('config', 'gatekeeper_secret_key')
app.server_name = config.get_string('config', 'hosts', 'gatekeeper')
app.session_cookie_domain = config.get_string('config', 'cookie_domain')
app.session_cookie_secure = True

KVSessionExtension(redis_store, app)

# Variable injections that should be available to all templates.
@app.context_processor
def injections():
    to_inject = {
        'bookmark_host': config.get_string('config', 'hosts', 'bookmark'),
        'signin_redirect': config.get_string('config', 'signin_redirect'),
        'static_url': static_url,
        'persist_url': persist_url
    }

    # Create a dummy csrf function for templates if debug is on.
    if config.get_boolean('config', 'debug'):
        to_inject['csrf_token'] = lambda: 0

    return to_inject

# Enabling CSRF protection seems to break
# automatic reloads on template changes.
#
# Do not enable protection in dev environments.
if not config.get_boolean('config', 'debug'):
    CsrfProtect(app)

@app.before_request
def pre_request():
    from modules.logger import log

    # Sessions should be permanent.
    session.permanent = True
    # Initialize the local cookie store.
    log.info('Received request.')
