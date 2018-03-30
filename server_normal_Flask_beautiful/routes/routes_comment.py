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
    token = request.args.get('token')
    if Comment.check_token(token, gg.csrf_tokens):
        form = request.form
        c = Comment.new(form, user_id=user.id, user_name=user.username)
        # c.save()
        # uid = c.tweet().user().id
        return redirect(url_for('tweet.detail', tweet_id=c.tweet_id, token=token))


@main.route('/delete/<int:comment_id>', methods=['GET'])
@login_required
def delete(comment_id):
    u = current_user()
    # comment_id = request.args.get('id', -1)
    # comment_id = int(comment_id)
    token = request.args.get('token')
    if Comment.check_token(token, gg.csrf_tokens):
        c = Comment.find(comment_id)
        if u.id == c.user_id:
            c.remove(comment_id)
        return redirect(url_for('tweet.detail', tweet_id=c.tweet_id, token=token))


@main.route('/edit/<int:comment_id>', methods=['GET'])
@login_required
def edit(comment_id):
    user = current_user()
    # comment_id = int(request.args.get('id', -1))
    token = request.args.get('token')
    if Comment.check_token(token, gg.csrf_tokens):
        c = Comment.find(comment_id)
        if user.id == c.user_id:
            body = render_template('tweet/comment_edit.html',
                            comment_id=c.id,
                            comment_content=c.content, token=token, u=user)
            return make_response(body)
        return redirect(url_for('tweet.detail', tweet_id=c.tweet_id, token=token, u=user))


@main.route('/update', methods=['POST'])
@login_required
def update():
    token = request.args.get('token')
    if Comment.check_token(token, gg.csrf_tokens):
        form = request.form
        Comment.check_id(form)
        newComment = Comment.update(form)
        # redirect有必要加query吗
        return redirect(url_for('tweet.detail', tweet_id=newComment.tweet_id, token=token))
