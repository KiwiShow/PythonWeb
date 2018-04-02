from models import MonModel, change_time
# from models.user import User
import models.user
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
