from models.user import User
from models.tweet import Tweet

from utils import log

from flask import (
    request,
    Blueprint,
    redirect,
    url_for,
    session,
    jsonify,
)
from routes import (
    login_required,
    current_user,
)

main = Blueprint('ajax_tweet', __name__)


@main.route('/index', methods=['GET'])
@login_required
def index():
    user_id = int(request.args.get('user_id', -1))
    if user_id == -1:
        u = current_user()
        user_id = u.id
    user = User.find(user_id)
    tweets = Tweet.find_all_json(user_id=user.id, deleted=False)
    return jsonify(tweets)


@main.route('/add', methods=['POST'])
@login_required
def add():
    user = current_user()
    form = request.json
    t = Tweet.new(form, user_id=user.id, user_name=user.username)
    return jsonify(t.json())


@main.route('/delete/<int:tweet_id>', methods=['GET'])
@login_required
def delete(tweet_id):
    # tweet_id = int(request.args.get('id'))
    t = Tweet.find_by(id=tweet_id)
    Tweet.check_id(id=tweet_id)
    Tweet.remove(tweet_id)
    # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
@login_required
def update():
    form = request.get_json()
    Tweet.check_id(form)
    newTweet = Tweet.update(form)
    return jsonify(newTweet.json())


# route_dict = {
#     '/ajax/tweet/index': login_required(index),
#     '/ajax/tweet/add': login_required(add),
#     '/ajax/tweet/delete': login_required(delete),
#     '/ajax/tweet/update': login_required(update),
#     # 评论功能
#     '/ajax/comment/index': login_required(comment_index),
#     '/ajax/comment/add': login_required(comment_add),
#     '/ajax/comment/delete': login_required(comment_delete),
#     '/ajax/comment/update': login_required(comment_update),
# }
