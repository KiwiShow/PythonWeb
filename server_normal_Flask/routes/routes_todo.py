from utils import log
from routes import (
    login_required,
    current_user,
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


@main.route('/edit', methods=['GET'])
def edit():
    todo_id = int(request.args.get('id'))
    t = Todo.find_by(id=todo_id)
    user = current_user()
    if user.id != t.user_id:
        return redirect(url_for('.index'))
    body = render_template('todo_edit.html', t=t)
    return make_response(body)


@main.route('/update', methods=['POST'])
def update():
    form = request.form
    Todo.check_id(form)
    newTodo = Todo.update(form)
    return redirect(url_for('.index'))


@main.route('/delete', methods=['GET'])
def delete():
    todo_id = int(request.args.get('id'))
    Todo.check_id(id=todo_id)
    Todo.remove(todo_id)
    return redirect(url_for('.index'))


@main.route('/status_switch', methods=['GET'])
def switch():
    todo_id = int(request.args.get('id'))
    Todo.check_id(id=todo_id)
    status = request.args.get('status')
    t = Todo.complete(todo_id, status)
    return redirect(url_for('.index'))
