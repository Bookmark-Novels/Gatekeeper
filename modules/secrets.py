import os
import json

from .object import Object
from .common import SECRETS_PATH

secrets = Object()

with open(SECRETS_PATH) as f:
    lines = ''.join(f.readlines())

    s = json.loads(lines)

    secrets.update(s)
