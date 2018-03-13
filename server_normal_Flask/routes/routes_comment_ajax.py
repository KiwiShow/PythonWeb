from models.user import User
from models.tweet import Tweet
from models.comment import Comment

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

main = Blueprint('ajax_comment', __name__)


@main.route('/index/<int:tweet_id>', methods=['GET'])
@login_required
def index(tweet_id):
    # tweet_id = int(request.args.get('tweet_id'))
    comments = Comment.find_all_json(tweet_id=tweet_id, deleted=False)
    return jsonify(comments)


@main.route('/add', methods=['POST'])
@login_required
def add():
    user = current_user()
    form = request.json
    c = Comment.new(form, user_id=user.id, user_name=user.username)
    # uid = c.tweet().user().id
    return jsonify(c.json())


@main.route('/delete/<int:comment_id>', methods=['GET'])
@login_required
def delete(comment_id):
    # comment_id = int(request.args.get('id'))
    t = Comment.find_by(id=comment_id)
    Comment.check_id(id=comment_id)
    Comment.remove(comment_id)
    # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
    return jsonify(t.json())


@main.route('/update', methods=['POST'])
@login_required
def update():
    form = request.get_json()
    Comment.check_id(form)
    newComment = Comment.update(form)
    return jsonify(newComment.json())
