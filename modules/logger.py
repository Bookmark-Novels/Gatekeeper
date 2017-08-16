import logging

import graypy

from .common import config, INSTANCE_NAME
from .secure import get_request_info

class BookmarkFilter(logging.Filter):
    def filter(self, record):
        info = get_request_info()
        record.__dict__.update(info)

log = logging.getLogger(INSTANCE_NAME)
log.setLevel(logging.INFO)

handler = graypy.GELFHandler(config.get_string('config', 'hosts', 'graylog'), config.get_integer('config', 'graylog', 'port'))
log.addHandler(handler)

log.addFilter(BookmarkFilter())
