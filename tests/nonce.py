import json
import os
import sys
import traceback

PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(PARENT)

from bookmark_database.models.instance import Instance
from bookmark_database.models.nonce import Nonce
from modules.secure import decrypt, encrypt

from app import app

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
        ), keyring.gatekeeper_key)
    })

    resp = json.loads(resp.get_data(as_text=True))

    assert 'nonce' in resp and resp['nonce'] != ''

def test_nonce_validity():
    resp = app.post('/nonce', data={
        'payload': encrypt(json.dumps(
            {
                'instance_id': INSTANCE_ID
            }
        ), keyring.gatekeeper_key)
    })

    resp = json.loads(resp.get_data(as_text=True))

    assert 'nonce' in resp and resp['nonce'] != ''

    nonce = decrypt(resp['nonce'], keyring.gatekeeper_key)

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

    esp = app.post('/nonce', data={'payload': encrypt('fsdoifjdsoifj', keyring.gatekeeper_key)}).status_code
    assert resp == 400

    esp = app.post('/nonce', data={'payload': encrypt('{"fdfdsf":"fsdfd"}', keyring.gatekeeper_key)}).status_code
    assert resp == 400

    resp = app.post('/nonce', data={
        'payload': encrypt(json.dumps(
            {
                'instance_id': 'fsdfsdfsdf'
            }
        ), keyring.gatekeeper_key)
    }).status_code
    assert resp == 400
