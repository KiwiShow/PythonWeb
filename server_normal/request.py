from utils import log
import urllib.parse


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
        log('from form --> form', self.body)
        # print('parsed body', body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        log('from form --> form(): ', f)
        return f

    def json(self):
        import json
        return json.loads(self.body)
