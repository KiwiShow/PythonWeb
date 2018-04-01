from models import MonModel, change_time
import time


class Board(MonModel):
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
    ]

    @classmethod
    def update(cls, form):
        board_id = int(form.get('id', -1))
        whitelist = ['id', 'title']
        Board.ori_update(whitelist, board_id, form)
