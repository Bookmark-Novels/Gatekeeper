import os
import uuid

import redis
from simplekv.decorator import PrefixDecorator
from simplekv.memory.redisstore import RedisStore

from bookmark_config import Config
from bookmark_database import config as _db_config
from locksmith import Locksmith

__all__ = ['APP_PATH', 'INSTANCE_NAME', 'INSTANCE_ID', 'config', 'redis_store']

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
INSTANCE_ID = str(uuid.uuid4())
INSTANCE_NAME = 'gatekeeper-{}'.format(INSTANCE_ID)

_consul_host = 'gatekeeper.consul.dev.bookmark.services'

if os.environ.get('ENV_StAGE') == 'PROD':
    _consul_host = 'gatekeeper.consul.bookmark.services'

_overrides = None
_override_path = os.path.join(APP_PATH, 'conf', 'overrides.json')

if os.path.isfile(_override_path):
    _overrides = _override_path

config = Config('gatekeeper.consul.dev.bookmark.services', 'gatekeeper', _overrides)

locksmith = Locksmith(config.get_string('config', 'vault_token'), config.get_string('config', 'hosts', 'vault'))
_db_user, _db_password = locksmith.get_credentials('bookmark')

_db_config.set_host(config.get_string('config', 'mysql', 'host'))
_db_config.set_user(_db_user)
_db_config.set_password(_db_password)
_db_config.set_database(config.get_string('config', 'mysql', 'database'))

redis_store = RedisStore(redis.StrictRedis(host=config.get_string('config', 'hosts', 'redis')))
redis_store = PrefixDecorator(config.get_string('config', 'redis_prefix'), redis_store)
