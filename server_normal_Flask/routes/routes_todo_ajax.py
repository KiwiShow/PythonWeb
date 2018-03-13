from utils import log
from routes import (
    login_required,
    current_user,
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


@main.route('/delete', methods=['GET'])
def delete():
    todo_id = int(request.args.get('id'))
    Todo.check_id(id=todo_id)
    Todo.remove(todo_id)
    t = Todo.find_by(id=todo_id)
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
def update():
    form = request.get_json()
    Todo.check_id(form)
    newTodo = Todo.update(form)
    return jsonify(newTodo.json())


@main.route('/status_switch', methods=['GET'])
def switch():
    todo_id = int(request.args.get('id'))
    Todo.check_id(id=todo_id)
    status = request.args.get('status')
    t = Todo.complete(todo_id, status)
    return jsonify(t.json())
