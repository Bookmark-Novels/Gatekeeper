import json
import os
import sys

PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(PARENT)

# Common must be imported first to initialize configuration values.
import modules.common

from bookmark_database.models.instance import Instance
from bookmark_database.models.nonce import Nonce

from modules.secure import decrypt, encrypt

from modules.app import app

# Import routes.
from routes import gatekeeper

app.testing = True
app = app.test_client()

INSTANCE_ID = 'test-instance'
INSTANCE_NAME = INSTANCE_ID

try:
    instance = Instance(instance_id=INSTANCE_ID, instance_name=INSTANCE_NAME)
    instance.save()
except:
    pass

def test_nonce_resp():
    resp = app.post('/nonce', data={
        'payload': encrypt(json.dumps(
            {
                'instance_id': INSTANCE_ID
            }
        ))
    })

    resp = json.loads(resp.get_data(as_text=True))

    assert 'nonce' in resp and resp['nonce'] != ''

def test_nonce_validity():
    resp = app.post('/nonce', data={
        'payload': encrypt(json.dumps(
            {
                'instance_id': INSTANCE_ID
            }
        ))
    })

    resp = json.loads(resp.get_data(as_text=True))

    assert 'nonce' in resp and resp['nonce'] != ''

    nonce = decrypt(resp['nonce'])

    assert Nonce.use(nonce, INSTANCE_ID)

def test_failing_nonce_use():
    assert not Nonce.use('fdsfdsfsd', INSTANCE_ID)

    nonce = Nonce.create(INSTANCE_ID)

    assert not Nonce.use(nonce, 'fosidfoisdjf')
    assert not Nonce.use(None, None)

def test_failing_nonce():
    resp = app.post('/nonce').status_code
    assert resp == 400

    resp = app.post('/nonce', data={'fosidjfodsijf': 'dsofidjfoi'}).status_code
    assert resp == 400

    resp = app.post('/nonce', data={'payload': 'dsofidjfoi'}).status_code
    assert resp == 400

    esp = app.post('/nonce', data={'payload': encrypt('fsdoifjdsoifj')}).status_code
    assert resp == 400

    esp = app.post('/nonce', data={'payload': encrypt('{"fdfdsf":"fsdfd"}')}).status_code
    assert resp == 400

    resp = app.post('/nonce', data={
        'payload': encrypt(json.dumps(
            {
                'instance_id': 'fsdfsdfsdf'
            }
        ))
    }).status_code
    assert resp == 400
