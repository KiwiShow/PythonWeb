from models.user import User
from models.tweet import Tweet
from models.comment import Comment
from routes import (
    login_required,
    current_user,
)

from utils import log
from flask import (
    request,
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    make_response,
    abort,
)
from config import gg


main = Blueprint('comment', __name__)


@main.route('/add', methods=['POST'])
@login_required
def add():
    """
    添加comment
    :return: 返回index页面
    """
    user = current_user()
    if Comment.check_token():
        form = request.form
        c = Comment.new(form, user_id=user.id, user_name=user.username)
        return redirect(url_for('tweet.detail', tweet_id=c.tweet_id, token=gg.token))


@main.route('/delete/<int:comment_id>', methods=['GET'])
@login_required
def delete(comment_id):
    if Comment.check_token():
        c = Comment.find(comment_id)
        Comment.check_id(id=comment_id)
        c.remove(comment_id)
        return redirect(url_for('tweet.detail', tweet_id=c.tweet_id, token=gg.token))


@main.route('/edit/<int:comment_id>', methods=['GET'])
@login_required
def edit(comment_id):
    user = current_user()
    if Comment.check_token():
        c = Comment.find(comment_id)
        Comment.check_id(id=comment_id)
        return render_template('tweet/comment_edit.html', c=c, token=gg.token, user=user)


@main.route('/update', methods=['POST'])
@login_required
def update():
    if Comment.check_token():
        form = request.form
        Comment.check_id(form)
        newComment = Comment.update(form)
        # redirect有必要加query吗
        return redirect(url_for('tweet.detail', tweet_id=newComment.tweet_id, token=gg.token))


@main.route('/like/<int:comment_id>', methods=['GET'])
@login_required
def like(comment_id):
    user = current_user()
    c = Comment.find(comment_id)
    if Comment.check_token():
        c.like(user.id)
        user.like_comment(comment_id)
        return redirect(url_for('tweet.detail', tweet_id=c.tweet().id, token=gg.token))


@main.route('/delike/<int:comment_id>', methods=['GET'])
@login_required
def delike(comment_id):
    user = current_user()
    c = Comment.find(comment_id)
    if Comment.check_token():
        c.delike(user.id)
        user.delike_comment(comment_id)
        return redirect(url_for('tweet.detail', tweet_id=c.tweet().id, token=gg.token))
