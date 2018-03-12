from flask import Flask

from routes.routes_user import main as user_routes
from routes.routes_static import main as route_static

# 为了符合WSGI，将应用包装成一个app，可以被WSGI服务端通过application(env, response)调用
app = Flask(__name__)

# 设置secret_key用来对称加密session
app.secret_key = 'Be the greatest，or nothing'

# 模块化路由的功能由 蓝图（Blueprints）提供
app.register_blueprint(user_routes)
app.register_blueprint(route_static)

# 运行
if __name__ == '__main__':
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)
