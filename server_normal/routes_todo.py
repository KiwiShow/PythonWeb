from utils import log, change_time
from models.todo import Todo
from routes import current_user, template, response_with_headers
from models.user import User
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


def redirect(url):
    headers = {
        'Location': url,
    }
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    # 以下代码 是选择 加载所有的todo 还是 某个用户专属的todo
    u = current_user(request)
    # todo_list = To_do.all()
    todo_list = Todo.find_all(user_id=u.id)
    todo_html = ''.join(['<h3>{} : {} created@{} updated@{} '
                         '<a href="/todo/edit?id={}">编辑</a> <a href="/todo/delete?id={}">删除</a>'.
                        format(t.id,
                               t.title,
                               change_time(t.created_time),
                               change_time(t.updated_time),
                               t.id,
                               t.id) for t in todo_list])
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
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
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))  # t.id是int，所以一定要str
    body = body.replace('{{todo_title}}', t.title)
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
    t.updated_time = int(time.time())
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
    else:
        user_list = u.all()
        user_html = ''.join(['<h3>id: {} username:{} password:{}</h3>'.format(t.id, t.username, t.password)
                             for t in user_list])
    body = template('admin.html')
    body = body.replace('{{users}}', user_html)
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
