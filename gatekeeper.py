from datetime import datetime, timedelta
import json

from flask import abort, jsonify, redirect, render_template, request, session, url_for

from app import app, bcrypt
from models.account import Account
from models.instance import Instance
from models.nonce import Nonce
from models.session import Session
from modules.cookie import delete_cookie, get_cookie, set_cookie
from modules.logger import log
from modules.secrets import hosts, keyring, secrets
from modules.secure import decrypt, encrypt, get_ip

'''
GATEKEEPER INTERACTION INTERFACE
'''

@app.route('/nonce', methods=['POST'])
def request_nonce():
    """Returns an encrypted nonce as a JSON response.

    The created nonce is bound to the requesting application's
    instance ID.

    Payload (Encrypted):
        {
            "instance_id": <string>
        }
    Response:
        {
            "nonce": <string | encrypted>
        }
    Raises:
        400: No payload provided/Invalid payload provided.
    """
    if 'payload' not in request.form:
        log('No payload provided.')
        abort(400)

    try:
        payload = decrypt(request.form['payload'], keyring.gatekeeper_key)
    except:
        log('Invalid payload provided: {}.'.format(request.form['payload']))
        abort(400)

    try:
        payload = json.loads(payload)
    except:
        log('Supplied payload is not valid JSON: {}.'.format(payload))
        abort(400)

    if 'instance_id' not in payload:
        log('Instance ID not present in payload.')
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
    """Returns a user's session key as an encrypted string.

    Payload (Encrypted):
        {
            "nonce": <string>,
            "origin": <string>
        }
    Response:
        {
            "session_key": <string | encrypted>
        }
    """
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

    if not Nonce.use(payload['nonce'], payload['origin']):
        log('Invalid nonce provided: <{}, {}>.'.format(payload['nonce'], payload['origin']))
        abort(400)

    if not get_cookie('gatekeeper_session'):
        return jsonify({
            'session_key': None
        })

    sess = Session.from_key(get_cookie('gatekeeper_session'))

    if sess is None or not sess.is_active:
        delete_cookie('gatekeeper_session')
        return jsonify({
            'session_key': None
        })

    sess.update_ip(get_ip())
    sess.use()

    return jsonify({
        'session_key': encrypt(get_cookie('gatekeeper_session'), keyring.gatekeeper_key)
    })

'''
GATEKEEPER PAGES
'''

@app.route('/', methods=['GET'])
def index():
    """You shouldn't be here. Redirect to Bookmark."""
    return redirect("https://" + hosts.bookmark)

@app.route('/signin', methods=['POST'])
def signin():
    """Attempts to sign the user in.

    Payload:
        {
            "email": <string>,
            "password": <string>
        }
    Response:
        {
            "redirect": <string>,
            "error": <string>
        }
    """
    if not get_cookie('gatekeeper_session'):
        if 'remove_limit_at' in session and session['remove_limit_at'] <= datetime.utcnow():
            del session['limit']
            del session['remove_limit_at']

        if 'limit' not in session:
            session['limit'] = secrets.max_attempts

        if session['limit'] == 0:
            return jsonify({
                'error': 'You have failed to log in more than {} times. Please try again later.'.format(secrets.max_attempts)
            })

        if 'email' not in request.form or 'password' not in request.form:
            return jsonify({
                'error': 'Email or password not specified.'
            })

        test = Account.from_email(request.form['email'])

        if test is None or not bcrypt.check_password_hash(test.password, request.form['password']):
            session['limit'] -= 1

            if session['limit'] == 0:
                session['remove_limit_at'] = datetime.utcnow() + timedelta(minutes=secrets.wait_minutes)

            return jsonify({
                'error': 'Invalid email or password specified.'
            })

        if not test.is_active:
            return jsonify({
                'error': 'This account has been disabled.'
            })

        session_key = Session.create(test.id, get_ip())
        set_cookie('gatekeeper_session', session_key)
        session['limit'] = secrets.max_attempts

    if 'next' in request.args:
        return jsonify({
            'redirect': request.args['next']
        })

    return jsonify({
        'redirect': secrets.signin_redirect
    })

@app.route('/signup', methods=['POST'])
def signup():
    """Attempts to create a new user account.

    Payload:
        {
            "name": <string>,
            "email": <string>,
            "password": <string>
        }
    Response:
        {
            "redirect": <string>,
            "error": <string>
        }
    """
    if not get_cookie('gatekeeper_session'):
        if 'name' not in request.form or 'email' not in request.form or 'password' not in request.form:
            return jsonify({
                'error': 'Name, email or password not specified.'
            })

        test = Account.from_email(request.form['email'])

        if test is not None:
            return jsonify({
                'error': 'An account with the password {} already exists.'.format(request.form['email'])
            })

        acc_id = Account.create(request.form['name'], request.form['email'], bcrypt.generate_password_hash(request.form['password']))
        session_key = Session.create(acc_id, get_ip())
        set_cookie('gatekeeper_session', session_key)

    if 'next' in request.args:
        return jsonify({
            'redirect': request.args['next']
        })

    return jsonify({
        'redirect': secrets.signin_redirect
    })

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    return render_template('template.html')

@app.route('/signout', methods=['GET'])
def signout():
    """Signs a user out. Deletes the user's `gatekeeper_session` cookie and invalidates the session server-side."""
    if not get_cookie('gatekeeper_session'):
        return redirect(url_for('signin'))

    session_key = get_cookie('gatekeeper_session')
    Session.from_key(session_key).invalidate()
    delete_cookie('gatekeeper_session')

    return redirect(url_for('signin'))

@app.route('/<path>', methods=['GET'])
def route_to_react(path):
    """Wildcard to send everything to React."""
    if get_cookie('gatekeeper_session'):
        return redirect(secrets.signin_redirect)

    return render_template('template.html')
