#!/usr/bin/env python3


import sys
from os.path import abspath
from os.path import dirname
import app

sys.path.insert(0, abspath(dirname(__file__)))

application = app.app


# print(dirname(__file__))
# print(abspath(dirname(__file__)))
# print(abspath(__file__))
# /Users/xxx/PycharmProjects/PythonWeb/server_normal_Flask
# /Users/xxx/PycharmProjects/PythonWeb/server_normal_Flask
# /Users/xxx/PycharmProjects/PythonWeb/server_normal_Flask/wsgi.py


# 建立一个软连接
# ln -s /root/PythonWeb/server_normal_Flask/newapp.conf /etc/supervisor/conf.d/newapp.conf
