from datetime import datetime, timedelta
import uuid

from flask import abort, jsonify, request, session, url_for

from app import app, bcrypt
from models.account import Account
from models.nonce import nonce
from models.session import Session
from modules.secure import get_ip
from secure import encrypt

@app.route('/', methods=['GET'])
def index():
    return redirect(secrets.default_redirect)

@app.route('/session', methods=['POST'])
def get_session():
    if 'gatekeeper_nonce' not in request.form:
        abort(403)

    if nonce.use(request.form['gatekeeper_nonce']):
        if 'gatekeeper_session' in session and Session.is_valid(session['gatekeeper_session']):
            return jsonify({
                'session_key': encrypt(session['gatekeeper_session'])
            })
        else:
            return jsonify({
                'session_key': None
            })
    else:
        abort(403)

@app.route('/login', methods=['GET'. 'POST'])
def login():
    if 'gatekeeper_session' in session:
        return redirect(url_for('index'))

    if 'limit' not in session:
        session['limit'] = secrets.max_attempts

    if request.method == 'POST':
        if session['limit'] == 0:
            if session['remove_limit_at'] > datetime.utcnow():
                flash(
                    'You have failed to log in more than {} times. Please try again later.'.format(secrets.max_attempts)
                )

        test = Account(email=request.form.email, password=bcrypt.hash_password(request.form.password))

        if test.is_authenticated():
            test.session_key = uuid.uuid4()
            test.ip_address = get_ip()
            test.save()

            session['gatekeeper_session'] = test.session_key
            session['limit'] = secrets.max_attempts

            if 'next' not in request.args:
                return redirect(secrets.default_redirect)
            else:
                return redirect(request.args['next'])
        else:
            if 'limit' in session:
                session['limit'] -= 1

                if session['limit'] == 0:
                    session['remove_limit_at'] = datetime.utcnow() + timedelta(minutes=secrets.wait_minutes)

            flash('Invalid email or password specified.')
            return render_template('index.html')
    else:
        # TODO: CSRF token generation. Check for CSRF on all POST requests.
        return render_template('login.html')