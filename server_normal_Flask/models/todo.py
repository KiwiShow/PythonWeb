from models.to_be_mongo import MonModel, change_time

import time


class Todo(MonModel):
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
        ('title', str, ''),
        ('user_id', int, ''),
        ('status', bool, False),
    ]

    @classmethod
    def complete(cls, id, completed):
        t = cls.find(id)
        t.status = completed
        t.save()
        return t

    @classmethod
    def update(cls, form):
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title')
        tm = int(time.time())
        t.updated_time = change_time(tm)
        t.save()
        return t


    # def change_time(self, t):
    #     format = '%Y/%m/%d %H:%M:%S'
    #     value = time.localtime(t)
    #     dt = time.strftime(format, value)
    #     return dt

# class Todo(Model):
#     def __init__(self, form, user_id=-1):
#         self.id = form.get('id', None)
#         self.title = form.get('title', '')
#         # 增加一个是否完成todo的属性
#         self.completed = False
#         # 增加 user_id 字段来和 User 类关联
#         self.user_id = form.get('user_id', -1)
#         # todo created_time还未改变
#         self.created_time = form.get('created_time', None)
#         self.updated_time = form.get('updated_time', None)
#         if self.created_time is None:
#             self.created_time = self.change_time(int(time.time()))
#             self.updated_time = self.created_time
#
#     @classmethod
#     def new(cls, form):
#         t = cls(form)
#         return t
#
#     @classmethod
#     def complete(cls, id, completed):
#         t = cls.find(id)
#         t.completed = completed
#         t.save()
#         return t
#
#     def change_time(self, t):
#         format = '%Y/%m/%d %H:%M:%S'
#         value = time.localtime(t)
#         dt = time.strftime(format, value)
#         return dt
