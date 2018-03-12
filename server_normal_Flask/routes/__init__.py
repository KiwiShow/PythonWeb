import random
from utils import log
from models.user import User
from models.todo import Todo
from models.tweet import Tweet
from models.comment import Comment
from flask import session



def random_str():
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)  # 其实减去1就可以
        s += seed[random_index]
    return s


def http_response(body):
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


# 增加一个函数集中处理headers的拼接,增强版本
def response_with_headers(headers, code=200):
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    headers = {
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def error(request, code=404):
    """
    根据 code 返回不同的错误响应
    目前只有 404
    """
    # 不要用数字来作为字典的 key
    # 但是在 HTTP 协议中 code 都是数字似乎更方便所以打破了这个原则
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


# 登录验证
def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u is None:
            log('from route_todo --> 非登录用户 redirect 到/login')
            return redirect('/login')
        else:
            return route_function(request)

    return f

# 身份验证
def check_id(request, form=None, id=None):
    if id == None:
        todo_id = int(form.get('id', -1))
    else:
        todo_id = id
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if u.id != t.user_id:
        return redirect('/login')

def check_id_tweet(request, form=None, id=None):
    if id == None:
        tweet_id = int(form.get('id', -1))
    else:
        tweet_id = id
    t = Tweet.find_by(id=tweet_id)
    u = current_user(request)
    if u.id != t.user_id:
        return redirect('/login')

def check_id_comment(request, form=None, id=None):
    if id == None:
        comment_id = int(form.get('id', -1))
    else:
        comment_id = id
    t = Comment.find_by(id=comment_id)
    u = current_user(request)
    if u.id != t.user_id:
        return redirect('/login')


# 获取当前的user实例
# 在jinja中用session全局变量
def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by(id=uid)
    return u
