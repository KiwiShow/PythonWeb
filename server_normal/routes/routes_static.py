def route_static(request):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        # 强制设置成Content - Type: image/gif，被坑了好久
        # header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        header = b'HTTP/1.1 200 OK\r\n'
        r = header + b'\r\n' + f.read()
        return r
