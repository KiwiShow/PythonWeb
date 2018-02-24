import socket


# 1. create socket
# 2. bind
# 3. listen
# 4. accept
# 5. recv
# 6. send
# 7. close -> 3

# 运行这个程序后, 浏览器打开 localhost:2000 就能访问了
# 一般浏览器默认2个连接GET / HTTP/1.1 和 GET /favicon.ico HTTP/1.1
s = socket.socket()
host = ''
port = 2000
s.bind((host, port))

while True:
    s.listen(5)
    print('before accept')
    # 当有客户端过来连接的时候, s.accept 函数就会返回 2 个值
    # 分别是 连接 和 客户端 ip 地址
    connection, address = s.accept()
    print('after accept')

    buf = b''
    while True:
        l = connection.recv(1024)
        buf += l
        if len(l) < 1024:
            break
    request = buf.decode('utf-8')
    print('客户端ip and request: {}\n{}'.format(address, request))

    response = b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>Hello, world</h1>'
    connection.sendall(response)
    connection.close()