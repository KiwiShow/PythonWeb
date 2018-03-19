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
    abort,
)

from models.to_be_mongo import change_time
from models.todo import Todo
import time
import uuid

main = Blueprint('todo', __name__)


# 对todo的CRUD绑定一个token
csrf_tokens = dict()


@main.route('/index', methods=['GET'])
@login_required
def index():
    """
    显示该用户所有todo
    :return: 显示todo页面
    """
    user = current_user()
    todo_list = Todo.find_all(user_id=user.id, deleted=False)
    # 用字典对每个todo进行token和user.id的匹配
    token = str(uuid.uuid4())
    csrf_tokens[token] = user.id
    body = render_template('todo_index.html', todos=todo_list, token=token)
    return make_response(body)


@main.route('/add', methods=['POST'])
@login_required
def add():
    """
    添加todo
    :return: 返回index页面
    """
    user = current_user()
    form = request.form
    token = request.args.get('token')
    if Todo.check_token(token, csrf_tokens):
        t = Todo.new(form, user_id=user.id)
        return redirect(url_for('.index'))


@main.route('/edit/<int:todo_id>', methods=['GET'])
@login_required
def edit(todo_id):
    # todo_id = int(request.args.get('id'))
    t = Todo.find_by(id=todo_id)
    user = current_user()
    if user.id != t.user_id:
        return redirect(url_for('.index'))
    token = request.args.get('token')
    if Todo.check_token(token, csrf_tokens):
        body = render_template('todo_edit.html', t=t, token=token)
        return make_response(body)


@main.route('/update', methods=['POST'])
@login_required
def update():
    form = request.form
    token = request.args.get('token')
    if Todo.check_token(token, csrf_tokens):
        Todo.check_id(form)
        newTodo = Todo.update(form)
        return redirect(url_for('.index'))


@main.route('/delete/<int:todo_id>', methods=['GET'])
@login_required
def delete(todo_id):
    # todo_id = int(request.args.get('id'))
    token = request.args.get('token')
    if Todo.check_token(token, csrf_tokens):
        csrf_tokens.pop(token)
        Todo.check_id(id=todo_id)
        Todo.remove(todo_id)
        return redirect(url_for('.index'))


# todo 修改
@main.route('/status_switch/<int:todo_id>', methods=['GET'])
@login_required
def switch(todo_id):
    # todo_id = int(request.args.get('id'))
    token = request.args.get('token')
    if Todo.check_token(token, csrf_tokens):
        Todo.check_id(id=todo_id)
        status = request.args.get('status')
        t = Todo.complete(todo_id, status)
        return redirect(url_for('.index'))
