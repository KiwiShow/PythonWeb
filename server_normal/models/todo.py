from models import Model
import time


class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        # 增加 user_id 字段来和 User 类关联
        self.user_id = form.get('user_id', -1)
        self.created_time = form.get('created_time', None)
        self.updated_time = form.get('updated_time', None)
        if self.created_time is None:
            self.created_time = int(time.time())
            self.updated_time = self.created_time
