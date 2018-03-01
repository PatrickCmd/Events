import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app.config import app_config
from app import app, db
from app.auth import models

config_name = os.environ.get('ENVIRONMENT_SETTINGS', 'development')
app.config.from_object(app_config.get(config_name))

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
