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
    return json_response(t.json())


route_dict = {
    '/ajax/todo/index': login_required(index),
    '/ajax/todo/add': login_required(add),
    '/ajax/todo/delete': login_required(delete),
}
