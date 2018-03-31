from models.user import User
from models.tweet import Tweet
from models.board import Board
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
from config import gg


main = Blueprint('tweet', __name__)


@main.route('/index', methods=['GET'])
# @login_required
def index():
    """
    显示该用户所有tweet
    :return: 显示tweet页面
    """
    user = current_user()
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        tweets = Tweet.find_all(deleted=False)
    else:
        tweets = Tweet.find_all(board_id=board_id, deleted=False)
    bs = Board.find_all(deleted=False)
    if user is not None:
        # 用字典对每个tweet进行token和user.id的匹配
        # token = str(uuid.uuid4())
        # csrf_tokens[token] = user.id
        # 保证每次调用index函数时清空gg
        gg.delete_value()
        # 保证每次调用index函数时都有新的token可用
        gg.set_value(user.id)
        log('from tweet',gg.csrf_tokens, gg.token)
        return render_template('tweet/tweet_index.html', tweets=tweets, token=gg.token, bs=bs, bid=board_id, user=user)
    else:
        return render_template('tweet/tweet_index.html', tweets=tweets, bs=bs, bid=board_id, user=user)


@main.route('/delete/<int:tweet_id>', methods=['GET'])
@login_required
def delete(tweet_id):
    u = current_user()
    # tweet_id = int(request.args.get('id'))
    token = request.args.get('token')
    if Tweet.check_token(token, gg.csrf_tokens):
        # gg.delete_value()
        # csrf_tokens.pop(token)
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
    user = current_user()
    token = request.args.get('token')
    board_id = int(request.args.get('board_id', -1))
    if Tweet.check_token(token, gg.csrf_tokens):
        bs = Board.find_all(deleted=False)
        return render_template('tweet/tweet_new.html', token=token, bs=bs, bid=board_id)


@main.route('/add', methods=['POST'])
@login_required
def add():
    user = current_user()
    token = request.args.get('token')
    board_id = int(request.args.get('board_id', -1))
    if Tweet.check_token(token, gg.csrf_tokens):
        form = request.form
        t = Tweet.new(form, user_id=user.id, user_name=user.username)
        # t.user_id = u.id
        # t.save()
        # redirect有必要加query吗
        # return redirect('/tweet/index?user_id={}'.format(user.id))
        return redirect(url_for('.index', board_id=board_id))


@main.route('/edit/<int:tweet_id>', methods=['GET'])
@login_required
def edit(tweet_id):
    user = current_user()
    token = request.args.get('token')
    if Tweet.check_token(token, gg.csrf_tokens):
    # tweet_id = int(request.args.get('id', -1))
        t = Tweet.find(tweet_id)
        if user.id == t.user_id:
            return render_template('tweet/tweet_edit.html', t=t, token=token)
        return redirect(url_for('.index'))


@main.route('/update', methods=['POST'])
@login_required
def update():
    token = request.args.get('token')
    if Tweet.check_token(token, gg.csrf_tokens):
        form = request.form
        Tweet.check_id(form)
        newTweet = Tweet.update(form)
        # redirect有必要加query吗
        return redirect(url_for('.index'))


@main.route('/detail/<int:tweet_id>', methods=['GET'])
# @login_required
def detail(tweet_id):
    user = current_user()
    t = Tweet.get(tweet_id)
    if user is not None:
        token = request.args.get('token')
        # tweet_id = int(request.args.get('id', -1))
        #     t = Tweet.find(tweet_id)
        # 这里不需要验证是否是自己发的tweet
        # if u.id == t.user_id:
        return render_template('tweet/tweet_detail.html', t=t, token=token, user=user)
    else:
        return render_template('tweet/tweet_detail.html', t=t, user=user)

