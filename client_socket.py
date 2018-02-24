import socket


# http层
# tcp udp
# socket是操作系统用来进行网络通信的底层方案
# 1. create socket
# 2. connect domain port
# 3. create request
# 4. unicode -> encode -> binary binary -> decode -> str
# 5. socket send
# 6. socket recv

# 参数 socket.AF_INET 表示是 ipv4 协议
# 参数 socket.SOCK_STREAM 表示是 tcp 协议
# 这是普通的 http socket,不是https，所以端口不能是443，只能是80
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#  以上2个参数为默认值，可以不写
s = socket.socket()
host = '163.com'
port = 80
# 参数是一个 tuple
s.connect((host, port))

ip, port = s.getsockname()
print('本机ip and port 是 {} {}'.format(ip, port))

# 构造request
request_str = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
request_bytes = request_str.encode('utf-8')
print('request_str: ', request_str)
print('request_bytes: ', request_bytes)
s.send(request_bytes)

# 组装response
response_bytes = b''
while True:
    buf = s.recv(1024)
    if not buf:
        break
    response_bytes += buf

response_str = response_bytes.decode('utf-8')
print('response_bytes: ', response_bytes)
print('response_str: ', response_str)