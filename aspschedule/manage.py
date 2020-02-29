from flask_migrate import MigrateCommand, Migrate
from flask_script import Manager
import os

from WestffsSchedules import create_app

# os.environ['FLASK_ENV'] = 'develop'

env = os.environ.get("FLASK_ENV") or 'default'

app = create_app(env)

manager = Manager(app=app)
# migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
