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
)


main = Blueprint('comment', __name__)


@main.route('/add', methods=['POST'])
@login_required
def add():
    """
    添加comment
    :return: 返回index页面
    """
    user = current_user()
    form = request.form
    c = Comment.new(form, user_id=user.id, user_name=user.username)
    # c.save()
    # uid = c.tweet().user().id
    return redirect(url_for('tweet.index'))


@main.route('/delete', methods=['GET'])
@login_required
def delete():
    u = current_user()
    comment_id = request.args.get('id', -1)
    comment_id = int(comment_id)
    c = Comment.find(comment_id)
    if u.id == c.user_id:
        c.remove(comment_id)
    return redirect(url_for('tweet.index'))


@main.route('/edit', methods=['GET'])
@login_required
def edit():
    u = current_user()
    comment_id = int(request.args.get('id', -1))
    c = Comment.find(comment_id)
    if u.id == c.user_id:
        body = render_template('comment_edit.html',
                        comment_id=c.id,
                        comment_content=c.content)
        return make_response(body)
    return redirect(url_for('tweet.index'))


@main.route('/update', methods=['POST'])
@login_required
def update():
    form = request.form
    Comment.check_id(form)
    newTweet = Comment.update(form)
    # redirect有必要加query吗
    return redirect(url_for('tweet.index'))
