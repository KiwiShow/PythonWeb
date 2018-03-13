from utils import log
from routes import (
    login_required,
    current_user,
    check_id,
)

from flask import (
    request,
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    make_response,
)

from models.to_be_mongo import change_time
from models.todo import Todo
import time


main = Blueprint('todo', __name__)


@main.route('/index', methods=['GET'])
def index():
    """
    显示该用户所有todo
    :return: 显示todo页面
    """
    user = current_user()
    todo_list = Todo.find_all(user_id=user.id, deleted=False)
    body = render_template('todo_index.html', todos=todo_list)
    return make_response(body)

# def index(request):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     # 以下代码 是选择 加载所有的todo 还是 某个用户专属的todo
#     u = current_user(request)
#     # todo_list = To_do.all()
#     todo_list = Todo.find_all(user_id=u.id, deleted=False)  # 如果删除就不现实出来
#     body = template('todo_index.html', todos=todo_list)
#     header = response_with_headers(headers)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


@main.route('/add', methods=['POST'])
def add():
    """
    添加todo
    :return: 返回index页面
    """
    user = current_user()
    form = request.form
    t = Todo.new(form, user_id=user.id)
    return redirect(url_for('.index'))


# def add(request):
#     u = current_user(request)
#     if request.method == 'POST':
#         form = request.form()
#         t = Todo.new(form, user_id=u.id)
#         # 进行权限绑定
#         # t.user_id = u.id
#         # t.save()
#     return redirect('/todo/index')


@main.route('/edit', methods=['GET'])
def edit():
    todo_id = int(request.args.get('id'))
    t = Todo.find_by(id=todo_id)
    user = current_user()
    if user.id != t.user_id:
        return redirect(url_for('.index'))
    body = render_template('todo_edit.html', t=t)
    return make_response(body)


# def edit(request):
#     headers = {
#         'Content-Type': 'text/html',
#     }
#     todo_id = int(request.query.get('id'))
#     t = Todo.find_by(id=todo_id)
#     u = current_user(request)
#     # 权限验证: 非授权用户不能更改
#     if u.id != t.user_id:
#         return redirect('/todo/index')
#     body = template('todo_edit.html', t=t)
#     header = response_with_headers(headers)
#     r = header + '\r\n' + body
#     return r.encode(encoding='utf-8')


@main.route('/update', methods=['POST'])
def update():
    form = request.form
    check_id(form)
    newTodo = Todo.update(form)
    return redirect(url_for('.index'))


# def update(request):
#     form = request.form()
#     check_id(request, form)
#     newTodo = Todo.update(form)
#     return redirect('/todo/index')


@main.route('/delete', methods=['GET'])
def delete():
    todo_id = int(request.args.get('id'))
    check_id(id=todo_id)
    Todo.remove(todo_id)
    return redirect(url_for('.index'))


# def delete(request):
#     todo_id = int(request.query.get('id'))
#     check_id(request, id=todo_id)
#     Todo.remove(todo_id)
#     return redirect('/todo/index')


@main.route('/status_switch', methods=['GET'])
def switch():
    todo_id = int(request.args.get('id'))
    check_id(id=todo_id)
    status = request.args.get('completed')
    t = Todo.complete(todo_id, status)
    return redirect(url_for('.index'))


# def switch(request):
#     todo_id = int(request.query.get('id'))
#     check_id(request, id=todo_id)
#     status = request.query.get('completed')
#     t = Todo.complete(todo_id, status)
#     return redirect('/todo/index')


# route_dict = {
#     '/todo/index': login_required(index),
#     '/todo/add': login_required(add),
#     '/todo/edit': login_required(edit),
#     '/todo/update': login_required(update),
#     '/todo/delete': login_required(delete),
#     '/todo/status_switch': login_required(switch),
# }
