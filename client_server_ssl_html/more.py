import socket
import ssl


def parsed_url(url):
    """
    手写url解析函数，有的函数本身美不起来，只能老老实实写
    :param url:
    :return: (protocol host port path)
    """
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # 检查默认 path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查端口
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if host.find(':') != -1:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个 socket 实例
    :param protocol:
    :return: socket实例
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        # HTTPS 协议需要使用 ssl.wrap_socket 包装一下原始的 socket
        # 除此之外无其他差别
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    """
    :param s: socket实例
    :return: 这个socket实例读取的所有数据(bytes)
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    """
    把 response 解析出 状态码 headers body
    :param r: response 是 str
    :return: 状态码 是 int; headers 是 dict; body 是 str
    """
    header, body = r.split('\r\n\r\n', 1)
    h = header.split('\r\n')
    status_code = h[0].split()[1]
    status_code = int(status_code)

    headers = {}
    for line in h[1:]:
        k, v = line.split(': ')
        headers[k] = v
    return status_code, headers, body


def get(url):
    """
    用 GET 请求 url 并返回响应，对301进行了处理
    :param url:
    :return:status_code, headers, body
    """
    protocol, host, port, path = parsed_url(url)

    s = socket_by_protocol(protocol)
    s.connect((host, port))

    request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    response = response_by_socket(s)
    r = response.decode(encoding)

    status_code, headers, body = parsed_response(r)
    if status_code == 301:
        url = headers['Location']
        return get(url)
    else:
        return status_code, headers, body


def log(*args, **kwargs):
    """
    用 log 代替 print
    :param args:
    :param kwargs:
    :return: 在前面多了标识符
    """
    print('log', *args, **kwargs)


# 实现函数
# def path_with_query(path, query):
#     url = path + '?'
#     for key, value in query.items():
#         url += key + '=' + str(value) + '&'
#     return url[:-1]


# 新的方法更pythonic
def path_with_query(path, query):
    q = []
    for key, value in query.items():
        cell = key + '=' + str(value)
        q.append(cell)
    return path + '?' + '&'.join(q)


# def test_path_with_query():
#     # 注意 height 是一个数字
#     path = '/'
#     query = {
#         'name': 'gua',
#         'height': 169,
#     }
#     expected = [
#         '/?name=gua&height=169',
#         '/?height=169&name=gua',
#     ]
#     # NOTE, 字典是无序的, 不知道哪个参数在前面, 所以这样测试
#     log(path_with_query(path, query))
#     assert path_with_query(path, query) in expected
#
# test_path_with_query()


# 为上课预习中的 get 函数增加一个参数 query
# query 是字典
# 比如
# url = https://movie.douban.com/top250
# query = {
#     'start': '25',
#     'filter': '',
# }
# get(url, query)
# get 函数中拼成如下的完整网址
# https://movie.douban.com/top250?start=25&filter=
# 注意, 因为字典不保证顺序, 所以 start 和 filter 的顺序无所谓



# def get(url, query):
#     protocol, host, port, path = parsed_url(url)
#
#     s = socket_by_protocol(protocol)
#     s.connect((host, port))
#
#     path = path_with_query(path, query)
#     url = path_with_query(url, query)
#     log(url)
#
#     request = 'GET {} HTTP/1.1\r\nhost: {}\r\nConnection: close\r\n\r\n'.format(path, host)
#     encoding = 'utf-8'
#     s.send(request.encode(encoding))
#
#     response = response_by_socket(s)
#     r = response.decode(encoding)
#
#     status_code, headers, body = parsed_response(r)
#     if status_code == 301:
#         url = headers['Location']
#         return get(url, query)
#     else:
#         return status_code, headers, body
#
#
# def test_get_with_query():
#
#     url = 'https://movie.douban.com/top250'
#     query = {
#         'start': '25',
#         'filter': '',
#     }
#
#     get(url, query)
#
# test_get_with_query()


# def header_from_dict(headers):
#     '''
#     headers 是一个字典
#     范例如下
#     对于
#     {
#         'Content-Type': 'text/html',
#         'Content-Length': 127,
#     }
#     返回如下 str
#     'Content-Type: text/html\r\nContent-Length: 127\r\n'
#     '''
#     header_str = []
#     for k, v in headers.items():
#         cell = k + ': ' + str(v)
#         header_str.append(cell)
#     return '\r\n'.join(header_str) + '\r\n'
#
#
# def test_header_from_dict():
#     headers = {
#         'Content-Type': 'text/html',
#         'Content-Length': 127,
#     }
#     log(header_from_dict(headers))
#     expected = [
#         'Content-Type: text/html\r\nContent-Length: 127\r\n',
#         'Content-Length: 127\r\nContent-Type: text/html\r\n',
#     ]
#
#     assert header_from_dict(headers) in expected
#
# test_header_from_dict()


# """
# 豆瓣电影 Top250 页面链接如下
# https://movie.douban.com/top250
# 我们的 client_ssl.py 已经可以获取 https 的内容了
# 这页一共有 25 个条目
#
# 得到页面的 html 内容
#
# # 提示 获取原始响应之后调用 parsed_response 得到的 body 就是 html 内容
# """


def parsed_one_page(url):
    status_code, headers, body = get(url)
    start_point = body.find('<ol class="grid_view">')
    stop_point = body.find('</ol>')
    msg = body[start_point:stop_point + 1].split('</li>')

    msg_all = []
    for m in msg[:25]:
        title_m_start_point = m.find('class="title"')
        title_m_stop_point = m[title_m_start_point:].find('</span>')
        title_m = m[title_m_start_point + 14:title_m_start_point + title_m_stop_point]

        rate_m_start_point = m.find('"v:average"')
        rate_m_stop_point = m[rate_m_start_point:].find('</span>')
        rate_m = m[rate_m_start_point + 12:rate_m_start_point + rate_m_stop_point]

        num_m_stop_point = m.find('人评价</span>')
        num_m_start_point = m[num_m_stop_point - 10:num_m_stop_point].find('>')
        num_m = m[num_m_stop_point - 10 + num_m_start_point + 1:num_m_stop_point]

        quote_m_start_point = m.find('class="inq"')
        if quote_m_start_point < 0:
            quote_m = 'No Quote!'
        else:
            quote_m_stop_point = m[quote_m_start_point:].find('</span>')
            quote_m = m[quote_m_start_point + 12:quote_m_start_point + quote_m_stop_point]

        value = ' title: ' + title_m + \
                ' rate: ' + rate_m + \
                ' num: ' + num_m + \
                ' quote: ' + quote_m

        msg_all.append(value)

    return msg_all


# log(parsed_one_page('https://movie.douban.com/top250'))


def get_all_page(url):
    query = {
        'start': 0,
    }
    # New_url = path_with_query(url,query)
    msg_all_page = []
    while True:
        new_url = path_with_query(url, query)
        msg_all_page.append(parsed_one_page(new_url))
        # log(msg_all_page)
        query['start'] = 25 * len(msg_all_page)
        if len(msg_all_page) == 10:
            break
    return msg_all_page


def test_get_all_page():
    url = 'https://movie.douban.com/top250'
    b = get_all_page(url)
    top_num = 1
    for i in b:
        for j in i:
            log('top' + str(top_num), j)
            top_num += 1


test_get_all_page()
