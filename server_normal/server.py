import socket
import urllib.parse
# TODO 了解thread（在python3中改名为_thread）,threading 和 queue模块 和 multiprocessing模块(for CPU密集型任务) 和 logging 模块
import _thread

from utils import log

from routes import route_static
from routes import route_dict
from routes_todo import route_dict as routes_todo

# server.py的整理思路
#     建立host和端口
#     监听请求
#     接受请求
#         分解请求信息
#             method
#             path
#             query
#             body
#         保存请求
#             临时保存，用完就丢
#     处理请求
#         获取路由字典
#             path和响应函数的映射字典
#         根据请求的path和字典处理请求并获得返回页面
#             routes
#                 主页
#                     返回页面
#                 登录
#                     处理post请求
#                         对比post数据和用户数据
#                         返回登录结果
#                     返回页面
#                 注册
#                     处理post请求
#                         对比post数据和注册规则
#                         保存合法的注册信息
#                             保存到User.txt
#                         返回注册结果
#                     返回页面
#                 留言板
#                     处理post请求
#                         将post的数据加入留言列表
#                     返回页面
#                         包含留言列表
#                 静态资源（图片）
#                     根据query的内容返回对应的资源
#         返回响应内容
#     发送响应内容
#     关闭请求连接


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self, request_data):
        r = request_data
        self.raw_data = r
        log('from __init__ --> Request log: ', r)
        self.method = r.split()[0]
        self.path = r.split()[1]
        self.body = r.split('\r\n\r\n', 1)[1]
        # 常用的str函数， split  strip  [:] join
        # get hand dirty 意思是不要看到好代码了，就自己不想写了，一定要把自己的想法提出来，慢慢提高

        self.query = {}
        self.headers = {}
        self.cookies = {}

        path, query = self.parsed_path()
        self.path = path
        self.query = query

        self.add_headers()
        self.add_cookies()
        log('from __init__ --> Request: path and query: ', path, query)

    def add_cookies(self):
        cookies = self.headers.get('Cookie', '')
        kvs = cookies.split('; ')
        log('from add_cookies --> cookie: ', kvs)
        for kv in kvs:
            if '=' in kv:
                k, v = kv.split('=')
                self.cookies[k] = v

    # 由parsed_header(raw_data)进化而来
    def add_headers(self):
        r = self.raw_data
        # 把 header 拿出来
        header = r.split('\r\n\r\n', 1)[0]
        lines = header.split('\r\n')[1:]
        # lines = header.split('\r\n')
        for line in lines:
            # log("error line", line)
            k, v = line.split(': ', 1)
            self.headers[k] = v

    # 由parsed_path(path)进化而来
    def parsed_path(self):
        path = self.path
        index = path.find('?')
        if index == -1:
            return path, {}
        else:
            path, query_string = path.split('?', 1)
            args = query_string.split('&')
            query = {}
            for arg in args:
                k, v = arg.split('=')
                query[k] = v
            return path, query

    def form(self):
        # 不解码加号
        body = urllib.parse.unquote(self.body)
        print('from form --> form', self.body)
        # print('parsed body', body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        print('from form --> form(): ', f)
        return f


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


def response_for_path(request):
    path = request.path
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    r.update(routes_todo)
    response = r.get(path, error)
    return response(request)


# 增加一个接收request的缓存函数
def request_cache(connection):
    buf = b''
    while True:
        cache = connection.recv(1024)
        buf += cache
        if len(cache) < 1024:
            break
    return buf.decode('utf-8')


def process_request(connection):
    r = request_cache(connection)
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        return
    # 设置 request 的 method
    request = Request(r)
    # chrome会发空请求，下面2行代码可以看出
    # log('r =====>', r)
    # log('r.split()=====>', r.split())
    # 用 response_for_path 函数来得到 path 对应的响应内容
    response = response_for_path(request)
    # 把响应发送给客户端
    connection.sendall(response)
    # 处理完请求, 关闭连接
    connection.close()


def run(host='', port=3000):
    """
    启动服务器
    """
    # 初始化 socket 套路
    # 使用 with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    log('from run --> start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
        # 使用 下面这句 可以保证程序重启后使用原有端口, 原因忽略
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            # 第二个参数类型必须是 tuple
            _thread.start_new_thread(process_request, (connection,))


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
