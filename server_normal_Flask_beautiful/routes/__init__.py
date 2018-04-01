from utils import log
from models.user import User
from flask import session, redirect, url_for, g
from functools import wraps

# 登录验证
# 本来想用g的，但是不太理解它的机制，所以。。。。。。
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_id', None) is None:
            log('from routes --> 非登录用户 redirect 到/login')
            return redirect(url_for('user.user_login'))
        return f(*args, **kwargs)
    return decorated_function


# 获取当前的user实例
# 在jinja中用session全局变量
def current_user():
    uid = session.get('user_id', -1)
    log("from current_user --> user_id : ", uid)
    u = User.find_by(id=uid)
    return u


# 验证机制
# 1.有无登陆 login_required
# 2.是否有权限(即是否自己的东西) check_id
# 3.是否是本人操作，防止CSRF 用token或者验证码(验证码还有防爬虫的功能)
# 4.验证是否是管理员
