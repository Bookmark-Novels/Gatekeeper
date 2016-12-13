from datetime import datetime, timedelta
import json
import uuid

from flask import abort, flash, jsonify, redirect, render_template, request, session, url_for

from app import app, bcrypt
from models.account import Account
from models.nonce import Nonce
from models.session import Session
from modules.cookie import get_cookie, set_cookie
from modules.secrets import secrets
from modules.secure import decrypt, encrypt, get_ip

@app.route('/', methods=['GET'])
def index():
    return render_template('/index.html')

@app.route('/session', methods=['POST'])
def get_session():
    if 'gatekeeper_nonce' not in request.form:
        abort(403)

    try:
        j = json.loads(decrypt(request.form['gatekeeper_nounce']))
        nounce = j['nounce']
        origin = j['origin']

        if nonce.use(nounce, origin):
            if get_cookie('gatekeeper_session') and Session.is_valid(get_cookie('gatekeeper_session')):
                return jsonify({
                    'session_key': encrypt(get_cookie('gatekeeper_session'))
                })
            else:
                return jsonify({
                    'session_key': None
                })
        else:
            abort(403)
    except:
        abort(403)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if get_cookie('gatekeeper_session'):
        return redirect(url_for('index'))

    if 'limit' not in session:
        session['limit'] = secrets.max_attempts

    if request.method == 'POST':
        if session['limit'] == 0:
            if session['remove_limit_at'] > datetime.utcnow():
                flash(
                    'You have failed to log in more than {} times. Please try again later.'.format(secrets.max_attempts)
                )

        test = Account.from_email(request.form['email'])

        if test is not None and bcrypt.check_password_hash(test.password, request.form['password']):
            test.session_key = uuid.uuid4()
            test.ip_address = get_ip()
            test.save()

            set_cookie('gatekeeper_session', test.session_key)
            session['limit'] = secrets.max_attempts

            if 'next' not in request.args:
                return redirect(secrets.login_redirect)
            else:
                return redirect(request.args['next'])
        else:
            if 'limit' in session:
                session['limit'] -= 1

                if session['limit'] == 0:
                    session['remove_limit_at'] = datetime.utcnow() + timedelta(minutes=secrets.wait_minutes)

            flash('Invalid email or password specified.')

    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/forgot-password')
def forgot_password():
    return render_template('forgot_password.html')