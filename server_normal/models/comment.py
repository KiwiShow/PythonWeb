from models import Model
from models.user import User
# from models.tweet import Tweet  # 这样不行
import models.tweet  # 为了避免和comment交叉引用


class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)
        # 注意一定要为int
        self.tweet_id = int(form.get('tweet_id', -1))

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def tweet(self):
        t = models.tweet.Tweet.find_by(id=self.tweet_id)
        return t
