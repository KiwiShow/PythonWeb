import os
from app import configured_app
from flask_script import Manager, Shell, Server


app = configured_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


def make_shell_context():
    return dict(app=app)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("runserver", Server(host="0.0.0.0", port=5000))


if __name__ == '__main__':
    manager.run()
