from models import MonModel, change_time
# from models.user import User
import models.user
# from models.tweet import Tweet  # 这样不行
import models.tweet  # 为了避免和comment交叉引用
import time

class Comment(MonModel):
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
        ('content', str, ''),
        ('user_id', int, -1),
        ('user_name', str, ''),
        ('tweet_id', int, -1),
    ]

    @classmethod
    def update(cls, form):
        comment_id = int(form.get('id', -1))
        whitelist = ['id', 'content', 'user_id', 'user_name', 'tweet_id']
        Comment.ori_update(whitelist, comment_id, form)
        return Comment.find_by(id=comment_id)

    def user(self):
        # u = User.find_by(id=self.json()['user_id'])
        # print('comments__dict__', self.__dict__)
        # print('comments__dict__.get("user_id")', self.__dict__.get('user_id'))
        # 以下2种写法都可以
        # u = User.find_by(id=self.__dict__.get('user_id'))
        u = models.user.User.find_by(id=self.user_id)
        # return u.json()['username']
        return u

    def tweet(self):
        t = models.tweet.Tweet.find_by(id=self.tweet_id)
        return t

# class Comment(Model):
#     def __init__(self, form, user_id=-1):
#         self.id = form.get('id', None)
#         self.content = form.get('content', '')
#         self.user_id = form.get('user_id', user_id)
#         # 注意一定要为int
#         self.tweet_id = int(form.get('tweet_id', -1))
#
#     def user(self):
#         u = User.find_by(id=self.user_id)
#         return u
#
#     def tweet(self):
#         t = models.tweet.Tweet.find_by(id=self.tweet_id)
#         return t
