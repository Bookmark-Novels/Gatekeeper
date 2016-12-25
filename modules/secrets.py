import os
import json

from .object import Object
from .common import HOSTS_PATH, INSTANCE_PATH, KEYRING_PATH, SECRETS_PATH

def load_obj(p, o):
    """Sets an Object's properties to mirror a given JSON file.

    Args:
        p: The path to the JSON file to use.
        o: The instance of Object to load `p` into.
    Raises:
        Any and all errors raised by json.loads when applicable.
    """
    with open(p) as f:
        lines = ''.join(f.readlines())
        s = json.loads(lines)
        o.update(s)

def config(p):
    """Returns a new Object with its properties as the contents of some JSON file.

    Args:
        p: The path to the JSON file to use.
    Raises:
        Any and all errors raised by json.loads when applicable.
    """
    o = Object()
    load_obj(p, o)
    return o

secrets = config(SECRETS_PATH)
hosts = config(HOSTS_PATH)
instance = config(INSTANCE_PATH)
keyring = config(KEYRING_PATH)
