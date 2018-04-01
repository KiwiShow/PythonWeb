from models import MonModel
from .todo import Todo
from .tweet import Tweet
from .comment import Comment
import hashlib
import time


class User(MonModel):
    """
    __fields__ = [
    '_id',
    ('id', int, -1),
    ('type', str, ''),
    ('deleted', bool, False),
    ('created_time', int, 0),
    ('updated_time', int, 0),
    """
    __fields__ = MonModel.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('note', str, '不要懒哦!'),
        ('role', int, 10),
        ('user_image', str, '/uploads/default.png'),
    ]

    @classmethod
    def update(cls, form):
        user_id = int(form.get('id', -1))
        user_password = form.get('password')
        password = User.salted_password(user_password)
        whitelist = ['id', 'username', 'password', 'note', 'role', 'user_image']
        # 因为form不可改变，而password需要加盐处理，所以只好额外传递一个参数password
        User.ori_update(whitelist, user_id, form, password=password)


    # def __init__(self, form):
    #     self.username = form.get('username', '')
    #     self.password = form.get('password', '')
    #     self.id = form.get('id', None)
    #     self.note = form.get('note', '')
    #     self.role = int(form.get('role', 10))
    @classmethod
    def salted_password(self, password, salt='less_is_more!'):
        def sha256(str):
            return hashlib.sha256(str.encode('utf-8')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    # 不加salt的password
    def hashed_password(self, pwd):
        p = pwd.encode('utf-8')
        s = hashlib.sha3_256(p)
        return s.hexdigest()

    @classmethod
    def validate_login(cls, form):
        # us = User.all()
        # for u in us:
        #     if self.username == u.username and self.password == u.password:
        #         return True
        # return False
        # 更加简洁
        user = User.find_by(username=form.get('username'))
        return user is not None and user.password == User.salted_password(form.get('password'))

    @classmethod
    def validate_register(cls, form):
        # 简单验证用户名或者密码长度必须大于2
        username = form.get('username', '')
        password = form.get('password', '')
        if User.find_by(username=username) is None and len(username) > 2 and len(password) > 2:
            u = User.new(form, password=User.salted_password(password))
            # u.password = u.salted_password(password)  # 加盐

            return True
        return False

    # 增加一个获取该user全部todo的函数 todo
    def todos(self):
        return Todo.find_all(user_id=self.id)

    # 增加一个获取该user全部有效tweet的函数
    def tweets(self):
        return Tweet.find_all(user_id=self.id)

    # 增加一个获取该user全部有效comment的函数
    def comments(self):
        return Comment.find_all(user_id=self.id)

    # 增加一个获取该user全部有效comment所对应的tweet且不重复的函数
    def uni_tweets(self):
        set1 = set([c.tweet().id for c in self.comments()])
        # print('set1        ',set)
        return [Tweet.find(i) for i in set1]

    # 增加一个验证是否是管理员
    @classmethod
    def check_admin(cls):
        from routes import current_user
        from flask import (
            redirect,
            url_for,
        )
        user = current_user()
        if user.id != 1:
            return redirect(url_for('.user_login'))
