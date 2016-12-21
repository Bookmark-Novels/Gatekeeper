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

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

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

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if get_cookie('gatekeeper_session'):
        return redirect(url_for('index'))

    if 'remove_limit_at' in session and session['remove_limit_at'] <= datetime.utcnow():
        del session['limit']

    if 'limit' not in session:
        session['limit'] = secrets.max_attempts

    if request.method == 'POST':
        if session['limit'] == 0:
            flash(
                'You have failed to log in more than {} times. Please try again later.'.format(secrets.max_attempts)
            )
            return render_template('signin.html')

        if 'email' not in request or 'password' not in request:
            log('Attempted to login without providing credentials: {}.', json.dumps(request.form))
            abort(400)

        test = Account.from_email(request.form['email'])

        if test is None or not bcrypt.check_password_hash(test.password, request.form['password']):
            session['limit'] -= 1

            if session['limit'] == 0:
                session['remove_limit_at'] = datetime.utcnow() + timedelta(minutes=secrets.wait_minutes)

            flash('Invalid email or password specified.')

        session_key = Session.create(test.id, get_ip())
        set_cookie('gatekeeper_session', test.session_key)
        session['limit'] = secrets.max_attempts

        if 'next' not in request.args:
            return redirect(secrets.signin_redirect)
        else:
            return redirect(request.args['next'])

    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')
