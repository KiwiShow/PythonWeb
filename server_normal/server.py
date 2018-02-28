import socket
import _thread
# TODO 了解thread（在python3中改名为_thread）,threading 和 queue模块 和 multiprocessing模块(for CPU密集型任务) 和 logging 模块

from utils import log
from request import Request

from routes import error
from routes.routes_static import route_static
from routes.routes_todo import route_dict as todo_routes
from routes.routes_user import route_dict as user_routes
from routes.routes_tweet import route_dict as tweet_routes


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


def response_for_path(request, r):
    path = request.path
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


def process_request(connection, r_d):
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
    response = response_for_path(request, r_d)
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
        # 字典放在这里在多线程的时候就不会重复构造了
        r_d = {
            '/static': route_static,
        }
        r_d.update(user_routes)
        r_d.update(todo_routes)
        r_d.update(tweet_routes)
        # 使用 下面这句 可以保证程序重启后使用原有端口, 原因忽略
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(5)
        # 无限循环来处理请求
        while True:
            connection, address = s.accept()
            # 第二个参数类型必须是 tuple
            _thread.start_new_thread(process_request, (connection, r_d))


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    run(**config)
