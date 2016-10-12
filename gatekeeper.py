from datetime import datetime, timedelta
import json
import uuid

from flask import abort, jsonify, request, session, url_for

from app import app, bcrypt
from models.account import Account
from models.nonce import nonce
from models.session import Session
from modules.cookie import cookie
from modules.secure import get_ip
from secure import decrypt, encrypt

@app.route('/', methods=['GET'])
def index():
    return redirect(secrets.default_redirect)

@app.route('/session', methods=['POST'])
def get_session():
    if 'gatekeeper_nonce' not in request.form:
        abort(403)

    try:
        j = json.loads(decrypt(request.form['gatekeeper_nounce']))
        nounce = j['nounce']
        origin = j['origin']
        
        if nonce.use(nounce, origin):
            if 'gatekeeper_session' in cookie and Session.is_valid(cookie['gatekeeper_session']):
                return jsonify({
                    'session_key': encrypt(cookie['gatekeeper_session'])
                })
            else:
                return jsonify({
                    'session_key': None
                })
        else:
            abort(403)
    except:
        abort(403)

@app.route('/login', methods=['GET'. 'POST'])
def login():
    if 'gatekeeper_session' in cookie:
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

            cookie['gatekeeper_session'] = test.session_key
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