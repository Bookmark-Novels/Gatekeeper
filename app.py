from modules.app import app as application
from modules.common import config
from routes import gatekeeper # pylint: disable=unused-import

if __name__ == '__main__':
    application.run(
        port=config.get_integer('config', 'port'),
        debug=config.get_boolean('config', 'debug')
    )
