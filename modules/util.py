import os

from .common import APP_PATH

def static_url(path):
    """Generates cache-busting URL for static resources.

    Args:
        path: A path corresponding to something within the `static` folder.
    Returns:
        A static path to the specified resource with the last-modified timestamp
        appended as a query argument.
    """
    timestamp = str(int(os.path.getmtime(os.path.join(APP_PATH, 'static', path))))
    return '/static/' + path + '?m=' + timestamp
