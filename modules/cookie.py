from flask import request, response

class Cookie(object):
    def __getattr__(self, name):
        if name in request.cookies:
            return request.cookies[name]
        else:
            return None
    
    def __setattr__(self, name, val):
        response.set_cookie(
            name,
            value=val,
            max_age=60 * 60 * 24 * 365,
            domain='*.{}'.format(secrets.bookmark_host)
        )

    def __contains__(self, name):
        return self[name] is not None

cookie = Cookie()