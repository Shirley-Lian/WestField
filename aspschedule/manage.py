from flask_script import Manager
import os
from WestffsSchedules import create_app
os.environ['FLASK_ENV'] = 'develop'

env = os.environ.get("FLASK_ENV") or 'default'
app = create_app(env)

manage = Manager(app=app)


if __name__ == '__main__':
    manage.run()
