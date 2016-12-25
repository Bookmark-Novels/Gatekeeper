import os

APP_PATH = os.path.abspath(os.path.dirname(__name__))
SECRETS_PATH = os.path.join(APP_PATH, 'conf', 'gatekeeper.json')
HOSTS_PATH = os.path.join(APP_PATH, 'conf', 'hosts.json')
INSTANCE_PATH = os.path.join(APP_PATH, 'conf', 'instance.json')
KEYRING_PATH = os.path.join(APP_PATH, 'conf', 'keyring.json')
