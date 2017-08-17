import json
import logging

import graypy

from .common import config, INSTANCE_NAME
from .secure import get_request_info

class BookmarkFilter(logging.Filter):
    def filter(self, record):
        info = get_request_info()
        record.context = json.dumps(info)
        return True

formatter = logging.Formatter('''[%(levelname)s] (%(asctime)s) %(name)s Message: %(message)s Context: %(context)s''')

log = logging.getLogger(INSTANCE_NAME)
log.setLevel(logging.INFO)

if config.get_string('stage') in ['beta', 'prod']:
    graylog_handler = graypy.GELFHandler(config.get_string('config', 'hosts', 'graylog'), config.get_integer('config', 'graylog', 'port'))
    graylog_handler.setLevel(logging.INFO)
    graylog_handler.setFormatter(formatter)
    log.addHandler(graylog_handler)
else:
    file_handler = logging.FileHandler(config.get_string('config', 'log_file'))
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)

log.addFilter(BookmarkFilter())
