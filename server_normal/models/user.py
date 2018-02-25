from models import Model


# 继承了 Model
# 所以可以直接 save load
class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.id = form.get('id', None)

    def validate_login(self):
        us = User.all()
        for u in us:
            if self.username == u.username and self.password == u.password:
                return True
        return False

    def validate_register(self):
        # 简单验证用户名或者密码长度必须大于2
        return len(self.username) > 2 and len(self.password) > 2