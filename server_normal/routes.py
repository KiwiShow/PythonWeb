from utils import log
from models.message import Message
from models.user import User

import random

# 这个函数用来保存所有的 messages
message_list = []
session = {}


def random_str():
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2) # 其实减去1就可以
        s += seed[random_index]
    return s

def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# 获取当前的user，若session里面没有，返回游客
def current_user(request):
    session_id = request.cookies.get('user', '')
    log("from current_user --> session id : ", session_id)
    log("from current_user --> session dict: ", session)
    username = session.get(session_id, '游客')
    return username


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    # 增加用户识别功能，并在主页显示名字
    username = current_user(request)
    body = body.replace('{{username}}', username)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 增加一个函数集中处理headers的拼接
def response_with_headers(headers):
    header = 'HTTP/1.1 200 OK\r\n'
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def route_login(request):
    headers = {
        'Content-Type': 'text/html',
    }
    log('from route_login --> cookies: ', request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            # 设置session_id
            session_id = random_str()
            log("from route_login --> session_id: ", session_id)
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = '请POST登录'
    body = template('login.html')
    body = body.replace('{{result}}', result)
    # 第一次输入用户名密码并提交{{username}}并不会改变，第一次提交cookie中还没有user字段而current_user需要根据这个判断
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_register(request):
    """
    POST /register HTTP/1.1
    Content-Type: x-www-form-urlencoded
    Host: localhost:3000

    username=gwgw&password=123
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '用户名或者密码长度必须大于2'
    else:
        result = '请POST注册'
    body = template('register.html')
    body = body.replace('{{result}}', result)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message(request):
    """
    主页的处理函数, 返回主页的响应
    """
    log('from route_message -->本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        # 增加一个存储功能 from kiwi
        # msg 和 message_list是2个不同的东西
        # msg是Message类的一个实例,msg.save()会将数据存入txt中
        # message_list是临时定义的空列表，其中元素是msg实例，每次启动会清零
        msg.save()
        # log('msg: type  ', type(msg))
        # log('msg: str   ', str(msg))
        # log('msg: ', msg)
        log('post', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('html_basic.html')
    # 列表推倒
    # 注意str(m) TODO
    msgs = '<br>'.join([str(m) for m in message_list])
    # 上面的列表推倒相当于下面的功能
    # messages = []
    # for m in message_list:
    #     messages.append(str(m))
    # msgs = '<br>'.join(messages)
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        r = header + b'\r\n' + f.read()
        return r


def route_profile(request):
    u = current_user(request)
    if u == '游客':
        header = 'HTTP/1.1 302 Temporarily Moved\r\nContent-Type: text/html\r\n' \
                 'Location: http://localhost:3000/login\r\n'
        body = template('login.html')
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')
    else:
        uname = User.find_by(username=u)
        header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
        body = '<h1>id:{} ' \
               'username: {} ' \
               'note: {}</h1>'.format(uname.id,
                                      uname.username,
                                      uname.note)
        r = header + '\r\n' + body
        return r.encode(encoding='utf-8')


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/profile': route_profile,
}
