import socket


# 1, 规范化生成响应
# 2, HTTP 头
# 3, 几个常用 HTML 标签及其用法
# 4, 参数传递的两种方式


def log(*args, **kwargs):
    """
    用 log 代替 print
    :param args:
    :param kwargs:
    :return: 在前面多了标识符
    """
    print('log', *args, **kwargs)


def html_content(path):
    with open(path, encoding='utf-8') as f:
        return f.read()


def route_index():
    '''
    主页的处理函数
    :return: 主页的响应
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello world</h1><img src="doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message():
    '''
    调用html_basic.html
    :return:
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = html_content('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_message_add():
    # 这个函数现在什么都干不了
    # 因为你没办法获取到浏览器传过来的数据
    form = dict(
        message='hello',
        author='gua',
    )
    header = 'HTTP/1.1 200 gua\r\nContent-Type: text/html\r\n'
    body = html_content('html_basic.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    '''
    图片的处理函数
    :return: 读取图片并生成响应返回
    '''
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


def error(code=404):
    '''
    根据 code 返回不同的错误响应
    目前只有 404
    :param code:
    :return: 错误响应
    '''
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n'
             b'Content-Type: text/html\r\n\r\n'
             b'<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'SORRY')


def response_for_path(path):
    '''
    根据 path 调用相应的处理函数
    没有处理的 path 会返回 404
    :param path:
    :return:
    '''
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/message': route_message,
        '/message/add': route_message_add,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    '''
    启动服务器
    :param host:
    :param port:
    :return:
    '''
    # 使用with 可以保证程序中断的时候正确关闭 socket 释放占用的端口
    with socket.socket() as go:
        go.bind((host, port))
        go.listen(5)
        while True:
            connection, address = go.accept()
            buf = b''
            while True:
                l = connection.recv(1024)
                buf += l
                if len(l) < 1024:
                    break
            request = buf.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.sendall(response)
            except Exception as e:
                log('error', e)
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=3000,
    )
    run(**config)