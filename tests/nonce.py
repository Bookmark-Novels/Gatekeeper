import json
import os
import sys
import traceback

PARENT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(PARENT)

import requests

from models.instance import Instance
from modules.secrets import hosts, keyring
from modules.secure import decrypt, encrypt

INSTANCE_ID = 'test-instance'
INSTANCE_NAME = INSTANCE_ID

try:
    instance = Instance(instance_id=INSTANCE_ID, instance_name=INSTANCE_NAME)
    instance.save()
except:
    pass

def test_nonce_resp():
    try:
        resp = requests.post('http://' + hosts.gatekeeper + '/nonce', {
            'payload': encrypt(json.dumps(
                {
                    'instance_id': INSTANCE_ID
                }
            ), keyring.gatekeeper_key)
        }).text

        resp = json.loads(resp)

        assert 'nonce' in resp and resp['nonce'] != ''
    except:
        traceback.print_exc()

def test_failing_nonce():
    try:
        resp = requests.post('http://' + hosts.gatekeeper + '/nonce').status_code
        assert resp == 400

        resp = requests.post('http://' + hosts.gatekeeper + '/nonce', {'fosidjfodsijf': 'dsofidjfoi'}).status_code
        assert resp == 400

        resp = requests.post('http://' + hosts.gatekeeper + '/nonce', {'payload': 'dsofidjfoi'}).status_code
        assert resp == 400

        esp = requests.post('http://' + hosts.gatekeeper + '/nonce', {'payload': encrypt('fsdoifjdsoifj', keyring.gatekeeper_key)}).status_code
        assert resp == 400

        esp = requests.post('http://' + hosts.gatekeeper + '/nonce', {'payload': encrypt('{"fdfdsf":"fsdfd"}', keyring.gatekeeper_key)}).status_code
        assert resp == 400

        resp = requests.post('http://' + hosts.gatekeeper + '/nonce', {
            'payload': encrypt(json.dumps(
                {
                    'instance_id': 'fsdfsdfsdf'
                }
            ), keyring.gatekeeper_key)
        }).status_code
        assert resp == 400
    except:
        traceback.print_exc()
