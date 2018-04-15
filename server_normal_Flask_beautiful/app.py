from flask import Flask

from routes.routes_user import main as user_routes
from routes.routes_static import main as static_routes
from routes.routes_todo import main as todo_routes
from routes.routes_tweet import main as tweet_routes
from routes.routes_comment import main as comment_routes
from routes.routes_board import main as board_routes
from routes.routes_mail import main as mail_routes
from routes.routes_error import main as error_routes

from utils import log
from config import  secret_key

from flask_bootstrap import Bootstrap


bootstrap = Bootstrap()


def configured_app():
    # 为了符合WSGI，将应用包装成一个app，可以被WSGI服务端通过application(env, response)调用
    app = Flask(__name__)

    # 设置secret_key用来对称加密session
    # 好处是不同的人用不同的secret_key，隔离开发和服务器环境，保证安全
    app.secret_key = secret_key
    # app.secret_key = 'Be the greatest，or nothing'
    bootstrap.init_app(app)
    register_routes(app)
    return app


def register_routes(app):
    # 模块化路由的功能由 蓝图（Blueprints）提供
    app.register_blueprint(user_routes)
    app.register_blueprint(static_routes)
    app.register_blueprint(todo_routes, url_prefix='/todo')
    app.register_blueprint(tweet_routes, url_prefix='/tweet')
    app.register_blueprint(comment_routes, url_prefix='/comment')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')
    app.register_blueprint(error_routes, url_prefix='/error')


# 运行
if __name__ == '__main__':
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5000,
    )
    log('from run --> start at', '{}:{}'.format(config['host'], config['port']))
    print('from run --> start at', '{}:{}'.format(config['host'], config['port']))
    app.run(**config)
