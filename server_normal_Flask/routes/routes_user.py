from utils import log
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
)
from models.message import Message
from models.user import User


main = Blueprint('todo', __name__)


@main.route('/', methods=['GET'])
def index():
    """
    主页的处理函数，如果登录，显示username，不然则显示游客
    :return: 主页
    """
    body = render_template('index.html', username='游客')
    user = current_user()
    if user is not None:
        body = render_template('index.html', username=user.username)
    r = make_response(body)
    return r


# def route_index(request):
#     """
#     主页的处理函数, 返回主页的响应
#     """
#     body = template('index.html', username='游客')
#     # 增加用户识别功能，并在主页显示名字
#     user = current_user(request)
#     log('routes_index ----> check current_user 返回值的type: ', user)
#     if user is not None:
#         body = template('index.html', username=user.username)
#     return http_response(body)


@main.route('/login', methods=['POST', 'GET'])
def login():
    """
    允许GET是因为在index页面转到login页面需要
    POST是因为在login页面输入账号密码点击login按钮需要
    主要的bug是在index和login页面都都是同一个路由函数
    :return:无论如何都会显示login页面
    """
    form = request.form
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
    return make_response(body)


# def route_login(request):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     log('from route_login --> cookies: ', request.cookies)
#     # 由cookie得到的用户实例,可能为None
#     u = current_user(request)
#     # 若有手动输入账号密码且用POST
#     # 2个 if 解决 有没有  和 对不对 的问题。
#     if request.method == 'POST':
#         form = request.form()
#         # 创建一个新的用户实例
#         if User.validate_login(form):
#             # 设置session_id
#             session_id = random_str()
#             log("from route_login --> session_id: ", session_id)
#             u = User.find_by(username=form.get('username'))
#             session[session_id] = u.id
#             headers['Set-Cookie'] = 'sid={}'.format(session_id)
#             result = '登录成功'
#         else:
#             result = '用户名或者密码错误'
#     else:
#         result = '请POST登录'
#     body = template('login.html', result=result, username='游客')
#     # 第一次输入用户名密码并提交{{username}}并不会改变，第一次提交cookie中还没有user字段而current_user需要根据这个判断
#     # 但是可以替换，如下代码所示
#     if u is not None:
#         body = body.replace('游客', u.username)
#     header = response_with_headers(headers)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


@main.route('/out')
def out():
    """
    在session中删除当前登录的user_id
    :return: 返回login页面
    """
    session.pop('user_id')
    return redirect(url_for('.login'))


# def route_out(request):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     session_id = request.cookies.get('sid', '')
#     if session_id != '':
#         session.pop(session_id)
#         result = '退出成功'
#     else:
#         result = '你还没登陆'
#     body = template('login.html', result=result, username='游客')
#     header = response_with_headers(headers)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


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


# def route_register(request):
#     """
#     POST /register HTTP/1.1
#     Content-Type: x-www-form-urlencoded
#     Host: localhost:3000
#
#     username=gwgw&password=123
#     """
#     if request.method == 'POST':
#         form = request.form()
#         # 这里既然有了form就不需要new了，如果new，会使id多加一次
#         # 不需要new之后，validate_register需要编成类方法
#         if User.validate_register(form):
#             result = '注册成功<br> <pre>{}</pre>'.format(User.all())
#         else:
#             result = '用户名或者密码长度必须大于2或者用户名已注册'
#     else:
#         result = '请POST注册'
#     body = template('register.html', result=result)
#     return http_response(body)


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


# def route_message(request):
#     """
#     主页的处理函数, 返回主页的响应
#     """
#     log('from route_message -->本次请求的 method', request.method)
#     if request.method == 'POST':
#         form = request.form()
#         msg = Message.new(form)
#         # 增加一个存储功能 from kiwi
#         # msg 和 message_list是2个不同的东西
#         # msg是Message类的一个实例,msg.save()会将数据存入txt中
#         # message_list是临时定义的空列表，其中元素是msg实例，每次启动会清零
#         # log('msg: type  ', type(msg))
#         # log('msg: str   ', str(msg))
#         # log('msg: ', msg)
#         log('post', form)
#         # 应该在这里保存 message_list
#     # 列表推倒
#     # 注意str(m)
#     msgs = '<br>'.join([str(m) for m in Message.all()])
#     # 上面的列表推倒相当于下面的功能
#     # messages = []
#     # for m in message_list:
#     #     messages.append(str(m))
#     # msgs = '<br>'.join(messages)
#     body = template('html_basic.html', messages=msgs)
#     return http_response(body)


@main.route('/profile', methods=['GET'])
def profile():
    """
    显示已登录用户的信息，木有模板
    :return: 返回含有已登录用户的信息
    """
    u = current_user()
    # html元素有效有效有效有效有效有效有效有效有效有效有效
    # 似乎render_template函数里面参数赋值的时候有过滤？
    # 在render_template中直接文本替代是不行的，只会当成字符串
    body = '<h1>id:{} ' \
           'username: {} ' \
           'note: {}</h1>'.format(u.id,
                                  u.username,
                                  u.note)
    return make_response(body)


# def route_profile(request):
#     u = current_user(request)
#     body = '<h1>id:{} ' \
#            'username: {} ' \
#            'note: {}</h1>'.format(u.id,
#                                   u.username,
#                                   u.note)
#     return http_response(body)


@main.route('/admin/users', methods=['GET'])
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


# def admin(request):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     u = current_user(request)
#     # 设定用户id=1是管理员进行权限验证
#     if u.id != 1:
#         return redirect('/login')
#     body = template('admin.html', users=u.all())
#     header = response_with_headers(headers)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


@main.route('/admin/user/update', methods=['POST'])
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


# def admin_update(request):
#     u = current_user(request)
#     # 设定用户id=1是管理员进行权限验证
#     if u.id != 1:
#         return redirect('/login')
#     form = request.form()
#     print(form.get('id', -1))
#     user_id = int(form.get('id', -1))
#     user_password = form.get('password', '')
#     user = User.find_by(id=user_id)
#     user.password = user.salted_password(user_password)
#     user.save()
#     return redirect('/admin/users')


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
