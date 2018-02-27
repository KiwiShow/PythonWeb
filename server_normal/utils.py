from jinja2 import Environment, FileSystemLoader
import os.path
import random
import time
from datetime import datetime


# 对print函数增强，增加了一个时间str
# 再次增强log函数，增加了输出到文本的功能
def log(*args, **kwargs):
    format_time = '%Y/%m/%d %H:%M:%S'
    # localtime()默认的是参数是time.time()
    value = time.localtime(int(time.time()))
    dt = time.strftime(format_time, value)
    # 对于No Newline at End of File的问题
    # set "Ensure line feed at file end on Save" under "Editor."
    with open('log.txt', 'a', encoding='utf-8') as f:
        # 不要用f=open() 和 f.close() 的组合，容易忘写 f.close()
        print(dt, *args, **kwargs, file=f)


def random_str():
    seed = 'bdjsdlkgjsklgelgjelgjsegker234252542342525g'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2) # 其实减去1就可以
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


# jinja模板增强
path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def template(path, **kwargs):
    t = env.get_template(path)
    return t.render(**kwargs)
