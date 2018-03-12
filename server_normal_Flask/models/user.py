from models.to_be_mongo import MonModel
from .todo import Todo
import hashlib


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
        ('note', str, ''),
        ('role', int, 10),
    ]

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
        ts = []
        for t in Todo.all():
            if t.user_id == self.json()['id']:
                ts.append(t)
        return ts
