from datetime import datetime, timedelta
import json

from flask import abort, flash, jsonify, redirect, render_template, request, session, url_for

from app import app, bcrypt
from models.account import Account
from models.instance import Instance
from modules.logger import log
from models.nonce import Nonce
from models.session import Session
from modules.cookie import get_cookie, set_cookie
from modules.secrets import secrets, keyring
from modules.secure import decrypt, encrypt, get_ip

'''
GATEKEEPER INTERACTION INTERFACE
'''

@app.route('/nonce', methods=['POST'])
def request_nonce():
    if 'payload' not in request.form:
        log('No payload provided.')
        abort(400)

    try:
        payload = decrypt(request.form['payload'], keyring.gatekeeper_key)
    except:
        log('Invalid payload provided: {}.'.format(payload))
        abort(400)

    try:
        payload = json.loads(payload)
    except:
        log('Supplied payload is not valid JSON: {}.'.format(payload))
        abort(400)

    if 'instance_id' not in payload:
        log('No payload provided.')
        abort(400)

    instance_id = payload['instance_id']

    if Instance.exists(instance_id):
        nonce = Nonce.create(instance_id)

        return jsonify({
            'nonce': encrypt(nonce, keyring.gatekeeper_key)
        })

    log('Invalid instance ID provided: {}.'.format(instance_id))
    abort(400)

@app.route('/session', methods=['POST'])
def get_session():
    if 'payload' not in request.form:
        log('No payload provided.')
        abort(400)

    try:
        payload = decrypt(request.form['payload'], keyring.gatekeeper_key)
    except:
        log('Invalid payload provided: {}.'.format(payload))
        abort(400)

    try:
        payload = json.loads(payload)
    except:
        log('Supplied payload is not valid JSON: {}.'.format(payload))
        abort(400)

    if 'nonce' not in payload:
        log('No nonce provided in payload.')
        abort(400)

    if 'origin' not in payload:
        log('No origin provided in payload.')
        abort(400)

    if not nonce.use(payload['nonce'], payload['origin']):
        log('Invalid nonce provided: <{}, {}>.', payload['nonce'], payload['origin'])
        abort(400)

    if not get_cookie('gatekeeper_session'):
        return jsonify({
            'session_key': None
        })

    session = Session.from_key(get_cookie('gatekeeper_session'))

    if session is None or not session.is_active:
        delete_cookie('gatekeeper_session')
        return jsonify({
            'session_key': None
        })

    session.update_ip(get_ip())
    session.use()

    return jsonify({
        # It should be noted that gatekeeper_session is already encrypted.
        'session_key': get_cookie('gatekeeper_session')
    })

'''
GATEKEEPER PAGES
'''

@app.route('/', methods=['GET'])
def index():
    return redirect(hosts.bookmark)

@app.route('/signin', methods=['POST'])
def signin():
    if not get_cookie('gatekeeper_session'):
        if 'remove_limit_at' in session and session['remove_limit_at'] <= datetime.utcnow():
            del session['limit']

        if 'limit' not in session:
            session['limit'] = secrets.max_attempts

        if session['limit'] == 0:
            return jsonify({
                'error': 'You have failed to log in more than {} times. Please try again later.'.format(secrets.max_attempts)
            })

        if 'email' not in request or 'password' not in request:
            log('Attempted to login without providing credentials: {}.', json.dumps(request.form))
            abort(400)

        test = Account.from_email(request.form['email'])

        if test is None or not bcrypt.check_password_hash(test.password, request.form['password']):
            session['limit'] -= 1

            if session['limit'] == 0:
                session['remove_limit_at'] = datetime.utcnow() + timedelta(minutes=secrets.wait_minutes)

            return jsonify({
                'error': 'Invalid email or password specified.'
            })

        session_key = Session.create(test.id, get_ip())
        set_cookie('gatekeeper_session', test.session_key)
        session['limit'] = secrets.max_attempts

    if 'next' not in request.args:
        return jsonify({
            'redirect': secrets.signin_redirect
        })
    else:
        return jsonify({
            'redirect': request.args['next']
        })

@app.route('/signup', methods=['POST'])
def signup():
    return render_template('template.html')

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    return render_template('template.html')

@app.route('/<wildcard>', methods=['GET'])
def route_to_react(wildcard):
    return render_template('template.html')
