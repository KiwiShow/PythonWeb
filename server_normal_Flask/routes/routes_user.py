from utils import log
from config import  image_file_dir, qiniu_up
from routes import (
    current_user,
    login_required,
)

from flask import (
    request,
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    make_response,
    send_from_directory,
)
from werkzeug.utils import secure_filename
import os
from models.message import Message
from models.user import User


main = Blueprint('user', __name__)


@main.route('/', methods=['GET'])
def index():
    """
    主页的处理函数，如果登录，显示username，不然则显示游客
    :return: 主页
    """
    body = render_template('index.html', username='游客')
    user = current_user()
    log('routes_index ----> check current_user 返回值的type: ', user)
    if user is not None:
        body = render_template('index.html', username=user.username)
    r = make_response(body)
    return r


@main.route('/login', methods=['POST', 'GET'])
def login():
    """
    允许GET是因为在index页面转到login页面需要
    POST是因为在login页面输入账号密码点击login按钮需要
    主要的bug是在index和login页面都都是同一个路由函数
    :return:无论如何都会显示login页面
    """
    form = request.form
    log('from route_login --> cookies: ', request.cookies)
    u = current_user()
    # ImmutableMultiDict([])是什么鬼？
    if form.get('username', None):
        if User.validate_login(form):
            u = User.find_by(username=form.get('username'))
            session['user_id'] = u.id
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = '请再登陆'
    body = render_template('login.html', result=result, username='游客')
    if u is not None:
        body = body.replace('游客', u.username)
        body = body.replace('请再登陆', '')
    return make_response(body)


@main.route('/out')
def out():
    """
    在session中删除当前登录的user_id
    :return: 返回login页面
    """
    session.pop('user_id')
    return redirect(url_for('.login'))


@main.route('/register', methods=['POST', 'GET'])
def register():
    """
    允许GET是因为在地址栏输入地址转到register页面需要
    POST是因为在register页面输入账号密码点击register按钮需要
    主要的bug是转到register页面和register页面都都是同一个路由函数
    :return: 返回register页面，并显示所有用户信息
    """
    result = ''
    form = request.form
    if request.method == 'POST':
        if User.validate_register(form):
            # html元素失效
            result = '注册成功'
        else:
            result = '用户名或者密码长度必须大于2或者用户名已注册'
    body = render_template('register.html', result=result, users=User.all())
    return make_response(body)


@main.route('/messages', methods=['POST', 'GET'])
def message():
    """
    允许GET是因为在地址栏输入地址转到messages页面需要
    POST是因为在messages页面内容点击"提交"按钮需要
    主要的bug是转到message页面和message页面都都是同一个路由函数
    :return: 返回message页面，并显示所有用户信息
    """
    form = request.form
    msg = Message.new(form)
    # html元素失效
    # msgs = '<br>'.join([str(m) for m in Message.all()])
    body = render_template('html_basic.html', messages=Message.all())
    return make_response(body)


@main.route('/profile', methods=['GET'])
@login_required
def profile():
    """
    显示已登录用户的信息，木有模板
    :return: 返回含有已登录用户的信息
    """
    u = current_user()
    # html元素有效有效有效有效有效有效有效有效有效有效有效
    # 似乎render_template函数里面参数赋值的时候有过滤？
    # 在render_template中直接文本替代是不行的，只会当成字符串
    body = render_template('profile.html', u=u)
    return make_response(body)


@main.route('/admin/users', methods=['GET'])
@login_required
def admin():
    """
    只有用户id为1的用户有权限
    :return: 返回所有用户的信息
    """
    u = current_user()
    if u.id != 1:
        return redirect(url_for('.login'))
    body = render_template('admin.html', users=u.all())
    return make_response(body)


@main.route('/admin/user/update', methods=['POST'])
@login_required
def admin_update():
    """
    只有用户id为1的用户有权限，输入需要修改的id和password
    :return: 返回修改过的所有用户的信息
    """
    u = current_user()
    if u.id != 1:
        return redirect(url_for('.login'))
    form = request.form
    user_id = int(form.get('id', -1))
    user_password = form.get('password', '')
    user = User.find_by(id=user_id)
    user.password = user.salted_password(user_password)
    user.save()
    return redirect(url_for('.admin'))


# 图片格式安全过滤
def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_image_file_type
    return suffix in accept_image_file_type


# 所有用户上传头像,先存在本地得到路径之后上传至七牛云，并删除本地图片
@main.route('/add_image', methods=['POST'])
@login_required
def add_img():
    u = current_user()
    file = request.files['avatar']
    if allow_file(file.filename):
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        filename = secure_filename(file.filename)
        # 2018/3/19/yiasduifhy289389f.png
        file.save(os.path.join(image_file_dir, filename))
        # u.add_avatar(filename)
        domain = qiniu_up(filename)
        os.remove(os.path.join(image_file_dir, filename))
        u.user_image = domain + filename
        u.save()
    return redirect(url_for('.profile'))


# web后端上传头像，后续可以改成Nginx+图床
# 本地只有default.png一张图片
@main.route('/uploads/<filename>')
@login_required
def uploads(filename):
    return send_from_directory(image_file_dir, filename)


# route_dict = {
#     '/': route_index,
#     '/login': route_login,
#     '/out': route_out,
#     '/register': route_register,
#     '/messages': route_message,
#     '/profile': login_required(route_profile),
#     '/admin/users': login_required(admin),
#     '/admin/user/update': login_required(admin_update),
# }
