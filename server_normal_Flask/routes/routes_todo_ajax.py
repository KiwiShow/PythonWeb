from utils import log
from routes import (
    login_required,
    current_user,
    check_id,
)
from flask import (
    request,
    Blueprint,
    redirect,
    url_for,
    session,
    make_response,
    jsonify,
)
from models.todo import Todo
import time


main = Blueprint('ajax_todo', __name__)


@main.route('/index', methods=['GET'])
def index():
    """
    显示该用户所有todo
    :return: 显示todo页面
    """
    user = current_user()
    todos = Todo.find_all_json(user_id=user.id, deleted=False)
    return jsonify(todos)


# def index(request):
#     u = current_user(request)
#     todos = Todo.find_all_json(user_id=u.id, deleted=False)
#     return json_response(todos)


@main.route('/add', methods=['POST'])
def add():
    """
    添加todo
    :return: 返回index页面
    """
    user = current_user()
    form = request.json
    t = Todo.new(form, user_id=user.id)
    return jsonify(t.json())


# def add(request):
#     u = current_user(request)
#     form = request.json()
#     t = Todo.new(form, user_id=u.id)
#     return json_response(t.json())


@main.route('/delete', methods=['GET'])
def delete():
    todo_id = int(request.args.get('id'))
    check_id(id=todo_id)
    Todo.remove(todo_id)
    t = Todo.find_by(id=todo_id)
    return jsonify(t.json())


# def delete(request):
#     todo_id = int(request.query.get('id'))
#     t = Todo.find_by(id=todo_id)
#     check_id(request, id=todo_id)
#     Todo.remove(todo_id)
#     # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
#     return json_response(t.json())


@main.route('/update', methods=['POST'])
def update():
    form = request.get_json()
    check_id(form)
    newTodo = Todo.update(form)
    return jsonify(newTodo.json())


# def update(request):
#     form = request.json()
#     check_id(request, form)
#     newTodo = Todo.update(form)
#     return json_response(newTodo.json())


@main.route('/status_switch', methods=['GET'])
def switch():
    todo_id = int(request.args.get('id'))
    check_id(id=todo_id)
    status = request.args.get('status')
    t = Todo.complete(todo_id, status)
    return jsonify(t.json())


# def switch(request):
#     todo_id = int(request.query.get('id'))
#     check_id(request, id=todo_id)
#     status = request.query.get('status')
#     t = Todo.complete(todo_id, status)
#     return json_response(t.json())


# route_dict = {
#     '/ajax/todo/index': login_required(index),
#     '/ajax/todo/add': login_required(add),
#     '/ajax/todo/delete': login_required(delete),
#     '/ajax/todo/update': login_required(update),
#     '/ajax/todo/status_switch': login_required(switch),
# }

# todo 权限验证和login_required可以用装饰器来做， 需要修改
# todo update等函数需要在类中定义，在这里每个函数内部只需要3步
# 1.拿数据
# 2.处理数据
# 3.返回数据
