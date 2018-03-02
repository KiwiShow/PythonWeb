from models.to_be_mongo import MonMondel


class Message(MonMondel):
    """
    __fields__ = [
    '_id',
    ('id', int, -1),
    ('type', str, ''),
    ('deleted', bool, False),
    ('created_time', int, 0),
    ('updated_time', int, 0),
    """
    __fields__ = MonMondel.__fields__ + [
        ('author', str, ''),
        ('message', str, ''),
    ]

# 定义一个 class 用于保存 message
# class Message(Model):
#     def __init__(self, form):
#         self.author = form.get('author', '')
#         self.message = form.get('message', '')
#         self.id = form.get('id', None)
