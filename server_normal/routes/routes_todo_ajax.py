from utils import log, template, json_response
from routes import (
    redirect,
    response_with_headers,
    login_required,
    current_user,
)
from models.to_be_mongo import change_time
from models.todo import Todo
import time


def index(request):
    u = current_user(request)
    todos = Todo.find_all_json(user_id=u.id, deleted=False)
    return json_response(todos)


def add(request):
    u = current_user(request)
    if request.method == 'POST':
        form = request.json()
        t = Todo.new(form, user_id=u.id)
    return json_response(t.json())


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if u.id != t.user_id:
        return redirect('/login')
    Todo.remove(todo_id)
    # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
    return json_response(t.json())


def update(request):
    form = request.json()
    todo_id = int(form.get('id', -1))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    if u.id != t.user_id:
        return redirect('/todo')
    t.title = form.get('title')
    # update时间
    tm = int(time.time())
    t.updated_time = change_time(tm)
    t.save()
    return json_response(t.json())

route_dict = {
    '/ajax/todo/index': login_required(index),
    '/ajax/todo/add': login_required(add),
    '/ajax/todo/delete': login_required(delete),
    '/ajax/todo/update': login_required(update),
}

# todo 权限验证和login_required可以用装饰器来做， 需要修改
# todo update等函数需要在类中定义，在这里每个函数内部只需要3步
# 1.拿数据
# 2.处理数据
# 3.返回数据
