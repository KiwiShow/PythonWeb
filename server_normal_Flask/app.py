from flask import Flask

from routes.routes_user import main as user_routes
from routes.routes_static import main as static_routes
from routes.routes_todo import main as todo_routes
from routes.routes_todo_ajax import main as todo_routes_ajax
from routes.routes_tweet import main as tweet_routes
# from routes.routes_tweet_ajax import main as tweet_routes_ajax
from routes.routes_comment import main as comment_routes


# 为了符合WSGI，将应用包装成一个app，可以被WSGI服务端通过application(env, response)调用
app = Flask(__name__)

# 设置secret_key用来对称加密session
app.secret_key = 'Be the greatest，or nothing'

# 模块化路由的功能由 蓝图（Blueprints）提供
app.register_blueprint(user_routes)
app.register_blueprint(static_routes)
app.register_blueprint(todo_routes, url_prefix='/todo')
app.register_blueprint(todo_routes_ajax, url_prefix='/ajax/todo')
app.register_blueprint(tweet_routes, url_prefix='/tweet')
# app.register_blueprint(tweet_routes_ajax, url_prefix='/ajax/tweet')
app.register_blueprint(comment_routes, url_prefix='/comment')


# 运行
if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)
