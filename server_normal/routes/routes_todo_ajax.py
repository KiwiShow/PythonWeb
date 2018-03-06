from utils import log, json_response
from routes import (
    redirect,
    response_with_headers,
    login_required,
    current_user,
    check_id,
)
from models.todo import Todo
import time


def index(request):
    u = current_user(request)
    todos = Todo.find_all_json(user_id=u.id, deleted=False)
    return json_response(todos)


def add(request):
    u = current_user(request)
    form = request.json()
    t = Todo.new(form, user_id=u.id)
    return json_response(t.json())


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)
    check_id(request, id=todo_id)
    Todo.remove(todo_id)
    # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
    return json_response(t.json())


def update(request):
    form = request.json()
    check_id(request, form)
    newTodo = Todo.update(form)
    return json_response(newTodo.json())


def switch(request):
    todo_id = int(request.query.get('id'))
    check_id(request, id=todo_id)
    status = request.query.get('status')
    t = Todo.complete(todo_id, status)
    return json_response(t.json())


route_dict = {
    '/ajax/todo/index': login_required(index),
    '/ajax/todo/add': login_required(add),
    '/ajax/todo/delete': login_required(delete),
    '/ajax/todo/update': login_required(update),
    '/ajax/todo/status_switch': login_required(switch),
}

# todo 权限验证和login_required可以用装饰器来做， 需要修改
# todo update等函数需要在类中定义，在这里每个函数内部只需要3步
# 1.拿数据
# 2.处理数据
# 3.返回数据
