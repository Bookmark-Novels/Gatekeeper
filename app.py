from modules.app import app as application
from routes import gatekeeper

if __name__ == '__main__':
    application.run(port=config.get_integer('config', 'port'), debug=config.get_boolean('config', 'debug'))
