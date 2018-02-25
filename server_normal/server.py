import socket
import urllib.parse
# TODO 了解thread（在python3中改名为_thread）,threading 和 queue模块 和 multiprocessing模块(for CPU密集型任务) 和 logging 模块
import _thread

from utils import log

from routes import route_static
from routes import route_dict


# 定义一个 class 用于保存请求的数据
class Request(object):
    def __init__(self):
        self.raw_data = ''
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}  # 按照作业加的

    def form(self):
        # 不解码加号
        body = urllib.parse.unquote(self.body)
        print('raw form', self.body)
        # print('parsed body', body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        print('form()', f)
        return f


# 定义一个parsed_header函数，以字典的形式保存了 HTTP 请求中的 header 区域的所有内容
def parsed_header(raw_data):
    header_part = raw_data.split('\r\n\r\n', 1)[0]
    lines = header_part.split('\r\n')
    headers = {}
    for line in lines[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return headers


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


def parsed_path(path):
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


def response_for_path(request):
    path = request.path
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('path and query', path, query)
    """
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    """
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def process_request(connection):
    r = connection.recv(1024)
    r = r.decode('utf-8')
    # log('ip and request, {}\n{}'.format(address, request))
    # 因为 chrome 会发送空请求导致 split 得到空 list
    # 所以这里判断一下防止程序崩溃
    if len(r.split()) < 2:
        return
    # 设置 request 的 method
    request = Request()
    request.raw_data = r
    # chrome会发空请求，下面2行代码可以看出
    # log('r =====>', r)
    # log('r.split()=====>', r.split())
    request.method = r.split()[0]
    request.path = r.split()[1]
    # 把 body 放入 request 中
    request.body = r.split('\r\n\r\n', 1)[1]
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
    log('start at', '{}:{}'.format(host, port))
    with socket.socket() as s:
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
        port=2000,
    )
    run(**config)
