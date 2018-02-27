from utils import log, redirect, response_with_headers, template
from models.todo import Todo
from models.user import User
from routes import current_user  # 不放在utils中放在routes中是因为一些变量只在routes.py中定义
import time


# 登录验证
def login_required(route_function):
    def f(request):
        u = current_user(request)
        if u is None:
            log('from route_todo --> 非登录用户 redirect 到/login')
            return redirect('/login')
        else:
            return route_function(request)
    return f


def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # 以下代码 是选择 加载所有的todo 还是 某个用户专属的todo
    u = current_user(request)
    # todo_list = To_do.all()
    todo_list = Todo.find_all(user_id=u.id)
    body = template('todo_index.html', todos=todo_list)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    u = current_user(request)
    if request.method == 'POST':
        form = request.form()
        t = Todo.new(form)
        # 进行权限绑定
        t.user_id = u.id
        t.save()
    return redirect('/todo')


def edit(request):
    headers = {
        'Content-Type': 'text/html',
    }
    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    # 权限验证: 非授权用户不能更改
    if u.id != t.user_id:
        return redirect('/todo')
    body = template('todo_edit.html', t=t)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def update(request):
    form = request.form()
    todo_id = int(form.get('id', -1))
    t = Todo.find_by(id=todo_id)
    u = current_user(request)
    # 权限验证: 非授权用户不能更改
    if u.id != t.user_id:
        return redirect('/todo')
    t.title = form.get('title')
    # update时间
    tm = int(time.time())
    t.updated_time = t.change_time(tm)
    t.save()
    return redirect('/todo')


def delete(request):
    todo_id = int(request.query.get('id'))
    t = Todo.find_by(id=todo_id)
    # 权限验证: 非授权用户不能更改
    u = current_user(request)
    if u.id != t.user_id:
        return redirect('/todo')
    Todo.remove(todo_id)
    return redirect('/todo')


def admin(request):
    headers = {
        'Content-Type': 'text/html',
    }
    u = current_user(request)
    # 设定用户id=1是管理员进行权限验证
    if u.id != 1:
        return redirect('/login')
    body = template('admin.html', users=u.all())
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def admin_update(request):
    u = current_user(request)
    # 设定用户id=1是管理员进行权限验证
    if u.id != 1:
        return redirect('/login')
    form = request.form()
    user_id = int(form.get('id', -1))
    user_password = form.get('password', '')
    user = User.find_by(id=user_id)
    user.password = user_password
    user.save()
    return redirect('/admin/users')


route_dict = {
    '/todo': login_required(index),
    '/todo/add': login_required(add),
    '/todo/edit': login_required(edit),
    '/todo/update': login_required(update),
    '/todo/delete': login_required(delete),
    '/admin/users': login_required(admin),
    '/admin/user/update': login_required(admin_update),
}
