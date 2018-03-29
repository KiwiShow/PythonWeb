#!/usr/bin/env python3


import sys
from os.path import abspath
from os.path import dirname
import app

sys.path.insert(0, abspath(dirname(__file__)))

# 这里变了骚年
application = app.configured_app()


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
