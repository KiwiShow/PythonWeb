from models.user import User
from models.tweet import Tweet
from models.comment import Comment

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
from routes import (
    login_required,
    current_user,
)
import uuid


main = Blueprint('tweet', __name__)


csrf_tokens = dict()


@main.route('/index', methods=['GET'])
@login_required
def index():
    """
    显示该用户所有tweet
    :return: 显示tweet页面
    """
    user_id = int(request.args.get('user_id', -1))
    if user_id == -1:
        u = current_user()
        user_id = u.id
    user = User.find(user_id)
    if user is None:
        return redirect(url_for('user.login'))
    else:
        # 用字典对每个tweet进行token和user.id的匹配
        token = str(uuid.uuid4())
        csrf_tokens[token] = user.id
        tweets = Tweet.find_all(user_id=user.id, deleted=False)
        body = render_template('tweet_index.html', tweets=tweets, user=user, token=token)
        return make_response(body)


@main.route('/delete/<int:tweet_id>', methods=['GET'])
@login_required
def delete(tweet_id):
    u = current_user()
    # tweet_id = int(request.args.get('id'))
    token = request.args.get('token')
    if Tweet.check_token(token, csrf_tokens):
        csrf_tokens.pop(token)
        t = Tweet.find(tweet_id)
        if u.id == t.user_id:
            # 这里只是删除了tweet，但是其所拥有的comment的deleted字段变成False
            t.remove(tweet_id)
            for c in t.comments():
                c.deleted = True
                c.save()
        # redirect有必要加query吗
        # return redirect('/tweet/index?user_id={}'.format(u.id))
        return redirect(url_for('.index'))


@main.route('/new', methods=['GET'])
@login_required
def new():
    token = request.args.get('token')
    if Tweet.check_token(token, csrf_tokens):
        body = render_template('tweet_new.html', token=token)
        return make_response(body)


@main.route('/add', methods=['POST'])
@login_required
def add():
    user = current_user()
    token = request.args.get('token')
    if Tweet.check_token(token, csrf_tokens):
        form = request.form
        t = Tweet.new(form, user_id=user.id, user_name=user.username)
        # t.user_id = u.id
        # t.save()
        # redirect有必要加query吗
        # return redirect('/tweet/index?user_id={}'.format(user.id))
        return redirect(url_for('.index'))


@main.route('/edit/<int:tweet_id>', methods=['GET'])
@login_required
def edit(tweet_id):
    u = current_user()
    token = request.args.get('token')
    if Tweet.check_token(token, csrf_tokens):
    # tweet_id = int(request.args.get('id', -1))
        t = Tweet.find(tweet_id)
        if u.id == t.user_id:
            body = render_template('tweet_edit.html',
                            tweet_id=t.id,
                            tweet_content=t.content, token=token)
            return make_response(body)
        return redirect(url_for('.index'))


@main.route('/update', methods=['POST'])
@login_required
def update():
    token = request.args.get('token')
    if Tweet.check_token(token, csrf_tokens):
        form = request.form
        Tweet.check_id(form)
        newTweet = Tweet.update(form)
        # redirect有必要加query吗
        return redirect(url_for('.index'))


# route_dict = {
#     '/tweet/index': login_required(index),
#     '/tweet/delete': login_required(delete),
#     '/tweet/edit': login_required(edit),
#     '/tweet/update': login_required(update),
#     '/tweet/add': login_required(add),
#     '/tweet/new': login_required(new),
    # 评论功能
    # '/comment/add': login_required(comment_add),
    # '/comment/delete': login_required(comment_delete),
    # '/comment/edit': login_required(comment_edit),
    # '/comment/update': login_required(comment_update),
# }
