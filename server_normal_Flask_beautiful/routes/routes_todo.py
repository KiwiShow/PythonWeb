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

from models import change_time
from models.todo import Todo
import time
from config import gg


main = Blueprint('todo', __name__)


@main.route('/index', methods=['GET'])
@login_required
def index():
    """
    显示该用户所有todo
    :return: 显示todo页面
    """
    user = current_user()
    gg.reset_value(user.id)
    log('from todo', gg.csrf_tokens, gg.token)
    return render_template('todo/new_todo_index.html', token=gg.token, user=user)


# 增加new路由函数去增加的页面
@main.route('/new', methods=['GET'])
@login_required
def new():
    user = current_user()
    if Todo.check_token():
        return render_template('todo/todo_new.html', token=gg.token, user=user)


@main.route('/add', methods=['POST'])
@login_required
def add():
    """
    添加todo
    :return: 返回index页面
    """
    user = current_user()
    if Todo.check_token():
        form = request.form
        t = Todo.new(form, user_id=user.id)
        return redirect(url_for('.index'))


@main.route('/edit/<int:todo_id>', methods=['GET'])
@login_required
def edit(todo_id):
    user = current_user()
    if Todo.check_token():
        # todo_id = int(request.args.get('id'))
        t = Todo.find_by(id=todo_id)
        Todo.check_id(id=todo_id)
        return render_template('todo/new_todo_edit.html', t=t, token=gg.token)


@main.route('/update', methods=['POST'])
@login_required
def update():
    if Todo.check_token():
        form = request.form
        Todo.check_id(form)
        Todo.update(form)
        return redirect(url_for('.index'))


@main.route('/delete/<int:todo_id>', methods=['GET'])
@login_required
def delete(todo_id):
    if Todo.check_token():
        Todo.check_id(id=todo_id)
        Todo.remove(todo_id)
        return redirect(url_for('.index'))


# todo 修改
@main.route('/status_switch/<int:todo_id>', methods=['GET'])
@login_required
def switch(todo_id):
    if Todo.check_token():
        Todo.check_id(id=todo_id)
        status = request.args.get('status')
        t = Todo.complete(todo_id, status)
        return redirect(url_for('.index'))
