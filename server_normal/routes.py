from utils import log
from models.message import Message
from models.user import User

message_list = []


def template(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = '请POST登录'
    body = template('login.html')
    body = body.replace('{{result}}', result)
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
    # import time
    # time.sleep(10)
    """
    主页的处理函数, 返回主页的响应
    """
    log('本次请求的 method', request.method)
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


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}
