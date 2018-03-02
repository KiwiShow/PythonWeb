from models.to_be_mongo import MonModel
from models.user import User
from models.comment import Comment


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
        ('content', str, ''),
        ('user_id', int, -1),
    ]

    # def comments(self):
    #     # return [c for c in Comment.all() if c.tweet_id == self.id]
    #     return Comment.find_all(tweet_id=self.json()['id'])
    #
    # def user(self):
    #     u = User.find_by(id=self.__dict__.get('user_id'))
    #     return u.json()['username']

    def comments(self):
        # return [c for c in Comment.all() if c.tweet_id == self.id]
        return Comment.find_all(tweet_id=self.id, deleted=False)

    def user(self):
        u = User.find_by(id=self.user_id)
        return u


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
