import os

from flask import request, url_for

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

def persist_url(route, *args, **kwargs):
    """Generates a route URL with the current request's query parameters appended to it.

    Args:
        route: The route to generate the URL for.
    Returns:
        A route URL with the current requests's query paramters appended to it.abs
    """
    if request.args:
        # Python 3.4 support.
        kwargs.update(request.args)
        return url_for(route, *args, **kwargs)
    return url_for(route)
