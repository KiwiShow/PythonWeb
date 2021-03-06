from models import MonModel, change_time
import models.user
from models.board import Board
from models.comment import Comment
import time

class Tweet(MonModel):
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
        ('views', int, 0),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('user_name', str, ''),
        ('who_likes', list, []),
    ]

    # def comments(self):
    #     # return [c for c in Comment.all() if c.tweet_id == self.id]
    #     return Comment.find_all(tweet_id=self.json()['id'])
    #
    # def user(self):
    #     u = User.find_by(id=self.__dict__.get('user_id'))
    #     return u.json()['username']
    @classmethod
    def update(cls, form):
        tweet_id = int(form.get('id', -1))
        whitelist = ['id', 'title', 'content', 'views', 'user_id', 'board_id', 'user_name', 'who_likes']
        Tweet.ori_update(whitelist, tweet_id, form)

    def like(self, id):
        self.who_likes.append(id)
        self.save()

    def delike(self, id):
        self.who_likes.remove(id)
        self.save()


    def comments(self):
        # return [c for c in Comment.all() if c.tweet_id == self.id]
        return Comment.find_all(tweet_id=self.id)

    def user(self):
        u = models.user.User.find_by(id=self.user_id)
        return u

    def board(self):
        u = Board.find_by(id=self.board_id)
        return u

    @classmethod
    def get(cls, id):
        t = cls.find(id)
        t.views += 1
        t.save()
        return t

    # 父类remove只是删除了tweet，但是其所拥有的comment的deleted字段变成False
    def remove_with_comments(self, id):
        self.remove(id)
        for c in self.comments():
            c.deleted = True
            c.save()

# class Tweet(Model):
#     def __init__(self, form, user_id=-1):
#         self.id = form.get('id', None)
#         self.content = form.get('content', '')
#         self.user_id = form.get('user_id', user_id)
#
#     def comments(self):
#         # return [c for c in Comment.all() if c.tweet_id == self.id]
#         return Comment.find_all(tweet_id=self.id)
#
#     def user(self):
#         u = User.find_by(id=self.user_id)
#         return u


# 不可在此文件中测试，因为路径的问题不能找到Tweet.txt和Comment.txt
# 需在与models平级的文件中测试
# def test_tweet():
#     # 用户 1 发微博
#     form = {
#         'content': 'hello tweet'
#     }
#     t = Tweet(form, 1)
#     t.save()
#     # 用户 2 评论微博
#     form = {
#         'content': '楼主说得对'
#     }
#     c = Comment(form, 2)
#     c.tweet_id = 1
#     c.save()
#     t = Tweet.find(1)
#     print('comments, ', t.comments())
#
#
# test_tweet()
