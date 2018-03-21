from flask import (
    request,
    Blueprint,
    render_template,
    redirect,
    url_for,
    make_response,
)


main = Blueprint('static', __name__)


@main.route('/static/<string:filename>')
def route_static(filename):
    """
    静态资源的处理函数, 读取图片并生成响应返回
    """
    # filename = request.args.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        # 强制设置成Content - Type: image/gif，被坑了好久
        # header = b'HTTP/1.1 200 OK\r\nContent-Type: image/gif\r\n'
        return make_response(f.read())
