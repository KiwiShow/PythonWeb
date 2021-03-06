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
    print('from todo_index  before', gg.csrf_tokens)
    gg.reset_value(user.id)
    print('from todo_index  after', gg.csrf_tokens)
    return render_template('todo/todo_index.html', token=gg.token[user.id], user=user)


# GET 去 new 页面， POST tweet_index 页面
@main.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    """
    添加todo
    :return: 返回index页面
    """
    user = current_user()
    if Todo.check_token():
        form = request.form
        if form.get('title'):
            t = Todo.new(form, user_id=user.id)
            return redirect(url_for('.index'))
        else:
            return render_template('todo/todo_new.html', token=gg.token[user.id], user=user)


@main.route('/edit/<int:todo_id>', methods=['GET'])
@login_required
def edit(todo_id):
    user = current_user()
    if Todo.check_token():
        # todo_id = int(request.args.get('id'))
        t = Todo.find_by(id=todo_id)
        Todo.check_id(id=todo_id)
        return render_template('todo/todo_edit.html', t=t, token=gg.token[user.id], user=user)


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


@main.route('/status_switch/<int:todo_id>', methods=['GET'])
@login_required
def switch(todo_id):
    if Todo.check_token():
        Todo.check_id(id=todo_id)
        status = request.args.get('status')
        t = Todo.complete(todo_id, status)
        return redirect(url_for('.index'))


@main.route('/detail/<int:todo_id>', methods=['GET'])
@login_required
def detail(todo_id):
    user = current_user()
    t = Todo.find(todo_id)
    if user is not None:
        # 保证每次调用index函数时清空gg,保证每次调用index函数时都有新的token可用
        print('from todo_datail  before', gg.csrf_tokens)
        gg.reset_value(user.id)
        print('from todo_datail  after', gg.csrf_tokens)
        return render_template('todo/todo_detail.html', t=t, token=gg.token[user.id], user=user)
    return render_template('todo/todo_detail.html', t=t, user=user)
