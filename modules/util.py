import os

from .common import APP_PATH

def static_url(path):
    timestamp = str(int(os.path.getmtime(os.path.join(APP_PATH, 'static', path))))
    return '/static/' + path + '?m=' + timestamp
