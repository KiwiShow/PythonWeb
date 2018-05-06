#!/usr/bin/env python3


import sys
import os
from os.path import abspath
from os.path import dirname
from app import configured_app

sys.path.insert(0, abspath(dirname(__file__)))

# 这里变了骚年
# wsgi 与 manage 分别是 生产环境(VPS) 和 开发环境 的 启动项， 都是输入  configured_app
# 还有问题： host port 设置了吗？
# wsgi 走的是 gunicorn.config.py 里面设置
application = configured_app(os.getenv('FLASK_CONFIG') or 'default')


# print(dirname(__file__))
# print(abspath(dirname(__file__)))
# print(abspath(__file__))
# /Users/xxx/PycharmProjects/PythonWeb/server_normal_Flask
# /Users/xxx/PycharmProjects/PythonWeb/server_normal_Flask
# /Users/xxx/PycharmProjects/PythonWeb/server_normal_Flask/wsgi.py


# 建立一个软连接 for webapp.conf
# ln -s /root/PythonWeb/server_normal_Flask_beautiful/webapp.conf /etc/supervisor/conf.d/webapp.conf
# 建立一个软连接 for webapp.nginx
# ln -s /root/PythonWeb/server_normal_Flask_beautiful/webapp.nginx /etc/nginx/sites-enabled/webapp
