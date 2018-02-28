from models import Model
from .todo import Todo
import hashlib

# 继承了 Model
# 所以可以直接 save load
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = form.get('id', None)
        self.note = form.get('note', '')
        self.role = int(form.get('role', 10))

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

    def validate_login(self):
        # us = User.all()
        # for u in us:
        #     if self.username == u.username and self.password == u.password:
        #         return True
        # return False
        # 更加简洁
        user = User.find_by(username=self.username)
        return user is not None and user.password == self.salted_password(self.password)

    def validate_register(self):
        # 简单验证用户名或者密码长度必须大于2
        if len(self.username) > 2 and len(self.password) > 2:
            self.password = self.salted_password(self.password)  # 加盐
            if User.find_by(username=self.username) is None:
                self.save()
                return True
        return False


    # 增加一个获取该user全部todo的函数
    def todos(self):
        ts =[]
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts
