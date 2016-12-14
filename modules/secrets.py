import os
import json

from .object import Object
from .common import HOSTS_PATH, INSTANCE_PATH, SECRETS_PATH

secrets = Object()
hosts = Object()
instance = Object()

with open(SECRETS_PATH) as f:
    lines = ''.join(f.readlines())

    s = json.loads(lines)

    secrets.update(s)

with open(HOSTS_PATH) as f:
    lines = ''.join(f.readlines())

    s = json.loads(lines)

    hosts.update(s)

with open(INSTANCE_PATH) as f:
    lines = ''.join(f.readlines())

    s = json.loads(lines)

    instance.update(s)