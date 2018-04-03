from models import MonModel, change_time
# from models.user import User
from routes import current_user
import models.user
from config import gg
import time


class Mail(MonModel):
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
        ('content', str, ''),
        ('sender_id', int, -1),
        ('receiver_id', int, -1),
        ('read_or_not', bool, False),
        ('sender_deleted', bool, False),
        ('receiver_deleted', bool, False),
    ]

    def set_sender(self, sender_id):
        self.sender_id = sender_id
        self.save()

    @classmethod
    def mark_read(cls, id):
        m = cls.find(id)
        m.read_or_not = True
        m.save()
        return m

    def to_user(self):
        u = models.user.User.find_by(id=self.receiver_id)
        return u

    def from_user(self):
        u = models.user.User.find_by(id=self.sender_id)
        return u

    @classmethod
    def update(cls, form):
        mail_id = int(form.get('id', -1))
        whitelist = ['id', 'title', 'content', 'sender_id', 'receiver_id', 'read']
        Mail.ori_update(whitelist, mail_id, form)
        return Mail.find_by(id=mail_id)

    @classmethod
    def receiver_sender_delete(cls, mail_id):
        from flask import redirect, url_for
        # 如果私信双方都已删除，不是真的删除
        # 只有管理员删除，那么就真的删除
        if current_user().id == 1:
            cls.remove(mail_id)
            return redirect(url_for('user.admin', token=gg.token))
        m = cls.find(mail_id)
        if current_user().id == m.receiver_id:
            cls.remove(mail_id, receiver_deleted=True)
        elif current_user().id == m.sender_id:
            cls.remove(mail_id, sender_deleted=True)
