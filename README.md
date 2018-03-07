# PythonWeb
> 用python开发web，一步一个脚印

### 1.简单的[client](https://github.com/KiwiShow/PythonWeb/blob/master/client_server_socket/client_socket.py)和[server](https://github.com/KiwiShow/PythonWeb/blob/master/client_server_socket/server_socket.py)

### 2.加强版本的[client](https://github.com/KiwiShow/PythonWeb/blob/master/client_server_ssl_html/client_ssl.py)和[server](https://github.com/KiwiShow/PythonWeb/blob/master/client_server_ssl_html/server_routes.py)

### 3.初步MVC的[server](https://github.com/KiwiShow/PythonWeb/tree/master/server_normal)

### 4.简单的`sqlite`和`MongoDB`数据库的练习[MongoDB](https://github.com/KiwiShow/PythonWeb/blob/todo_jinja/mongo_sqlite/mongo_demo.py)和[sqlite](https://github.com/KiwiShow/PythonWeb/blob/todo_jinja/mongo_sqlite/sqlite_demo.py)


## **简单说说初步MVC的`server`，在文件夹`server_normal`中。**
包含的功能：
1.用户管理(没有用户删除功能)
```python
route_dict = {
    '/': route_index,欢迎界面。有1个login链接
    '/login': route_login,登陆界面，登陆成功该界面刷新一些信息，不跳转。有2个链接分别去该用户的todo界面和tweet界面，有2个链接分别是数据api
    '/register': route_register,注册界面，注册成功该界面刷新一些信息，不跳转。
    '/messages': route_message,演示表单提交的页面，显示所有message
    '/profile': login_required(route_profile),该用户的id name password
    '/admin/users': login_required(admin),id为1的admin用户可以看所有用户id name password
    '/admin/user/update': login_required(admin_update),id为1的admin用户可以更改所有用户password
}
```
2.`todo`操作
> `index`界面，分别用`http`页面刷新方式和`ajax`方式显示。可对`todo`进行`CRUD`，也可以更改`todo`状态。
```python
route_dict = {
    '/todo/index': login_required(index),
    '/todo/add': login_required(add),
    '/todo/edit': login_required(edit),
    '/todo/update': login_required(update),
    '/todo/delete': login_required(delete),
    '/todo/status_switch': login_required(switch),
}
```
> api接口
```python
route_dict = {
    '/ajax/todo/index': login_required(index),
    '/ajax/todo/add': login_required(add),
    '/ajax/todo/delete': login_required(delete),
    '/ajax/todo/update': login_required(update),
    '/ajax/todo/status_switch': login_required(switch),
}
```
3.`tweet`和`comment`操作
>`index`界面，分别用`http`页面刷新方式和`ajax`方式显示。可对`tweet`和`comment`进行CRUD
除了使用`ajax`api的`comment`不会根据`user_id`改变外，
`http`的`tweet`和`comment`以及`ajax`api的`tweet`可以根据`user_id`显示，并有用户验证功能
验证规则是:自己只能删除自己的东西(`tweet`和`comment`)
```python
route_dict = {
    '/tweet/index': login_required(index),
    '/tweet/delete': login_required(delete),
    '/tweet/edit': login_required(edit),
    '/tweet/update': login_required(update),
    '/tweet/add': login_required(add),
    '/tweet/new': login_required(new),
    '/comment/add': login_required(comment_add),
    '/comment/delete': login_required(comment_delete),
    '/comment/edit': login_required(comment_edit),
    '/comment/update': login_required(comment_update),
}
```
> api接口
```python
route_dict = {
    '/ajax/tweet/index': login_required(index),
    '/ajax/tweet/add': login_required(add),
    '/ajax/tweet/delete': login_required(delete),
    '/ajax/tweet/update': login_required(update),
    '/ajax/comment/index': login_required(comment_index),
    '/ajax/comment/add': login_required(comment_add),
    '/ajax/comment/delete': login_required(comment_delete),
    '/ajax/comment/update': login_required(comment_update),
}
```
4.简单的`cookie`和`session`功能

## **相关技术**
1.前端用到了`html`，`ajax`和`jinja`模板渲染
2.后端未使用任何框架。基于`socket`手工打造
3.数据存储有`txt`接口和`MongoDB`接口

