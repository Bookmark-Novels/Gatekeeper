import logging

import graypy

from .secrets import secrets, instance
from .secure import get_request_info

class BookmarkFilter(logging.Filter):
    def filter(self, record):
        info = get_request_info()
        info.update(secrets.graylog.static_fields)

        record.__dict__.update(get_request_info())

log = logging.getLogger(instance.instance_name)
log.setLevel(logging.INFO)

handler = graypy.GELFHandler(secrets.graylog.host, secrets.graylog.port)
log.addHandler(handler)

log.addFilter(BookmarkFilter())
