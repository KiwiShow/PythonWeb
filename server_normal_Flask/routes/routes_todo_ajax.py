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
    jsonify,
)
from models.todo import Todo
import time


main = Blueprint('ajax_todo', __name__)


@main.route('/index', methods=['GET'])
@login_required
def index():
    """
    显示该用户所有todo
    :return: 显示todo页面
    """
    user = current_user()
    todos = Todo.find_all_json(user_id=user.id, deleted=False)
    return jsonify(todos)


@main.route('/add', methods=['POST'])
@login_required
def add():
    """
    添加todo
    :return: 返回index页面
    """
    user = current_user()
    form = request.json
    t = Todo.new(form, user_id=user.id)
    return jsonify(t.json())


@main.route('/delete/<int:todo_id>', methods=['GET'])
@login_required
def delete(todo_id):
    # todo_id = int(request.args.get('id'))
    Todo.check_id(id=todo_id)
    Todo.remove(todo_id)
    t = Todo.find_by(id=todo_id)
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
@login_required
def update():
    form = request.get_json()
    Todo.check_id(form)
    newTodo = Todo.update(form)
    return jsonify(newTodo.json())


# todo, status可否再作为一个动态路由里面的参数？
@main.route('/status_switch/<int:todo_id>', methods=['GET'])
@login_required
def switch(todo_id):
    # todo_id = int(request.args.get('id'))
    Todo.check_id(id=todo_id)
    status = request.args.get('status')
    t = Todo.complete(todo_id, status)
    return jsonify(t.json())
