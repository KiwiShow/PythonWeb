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
    tweets_and_boards,
)
from config import gg


main = Blueprint('tweet', __name__)


# 几个问题
# 1.什么时候验证login_required？
# 数据的CRUD的时候需要验证，这里包括去CRUD的页面。不login，这些页面去不了。
# 对于index页面，在没有login的时候也能显示，但是有些按钮元素不显示，这需要靠 user = current_user()判断
# 2.什么时候初始化一个新的token？
# 在index的时候, Tweet，待办事项，Mail， profile，setting
@main.route('/index', methods=['GET'])
# @login_required
def index():
    """
    显示该用户所有tweet
    :return: 显示tweet页面
    """
    user = current_user()
    board_id = int(request.args.get('board_id', -1))
    current_page = int(request.args.get('page', 1))
    tweets, bs, pages = tweets_and_boards(board_id, current_page)
    if user is not None:
        # 保证每次调用index函数时清空gg,保证每次调用index函数时都有新的token可用
        print('from tweet  before', gg.csrf_tokens)
        gg.reset_value(user.id)
        print('from tweet  after', gg.csrf_tokens)
        return render_template('tweet/tweet_index.html', current_page=current_page, pages = range(pages), tweets=tweets, bs=bs, bid=board_id, user=user, token=gg.token[user.id])
    return render_template('tweet/tweet_index.html', pages = range(pages), tweets=tweets, bs=bs, bid=board_id, user=user)


@main.route('/delete/<int:tweet_id>', methods=['GET'])
@login_required
def delete(tweet_id):
    if Tweet.check_token():
        t = Tweet.find(tweet_id)
        Tweet.check_id(id=tweet_id)
        t.remove_with_comments(tweet_id)
        return redirect(url_for('.index'))


@main.route('/new', methods=['GET'])
@login_required
def new():
    user = current_user()
    board_id = int(request.args.get('board_id', -1))
    if Tweet.check_token():
        bs = Board.find_all()
        return render_template('tweet/tweet_new.html', token=gg.token[user.id], bs=bs, board_id=board_id, user=user)


@main.route('/add', methods=['POST'])
@login_required
def add():
    user = current_user()
    board_id = int(request.args.get('board_id', -1))
    if Tweet.check_token():
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
    if Tweet.check_token():
    # tweet_id = int(request.args.get('id', -1))
        t = Tweet.find(tweet_id)
        Tweet.check_id(id=tweet_id)
        return render_template('tweet/tweet_edit.html', t=t, token=gg.token[user.id], user=user)


@main.route('/update', methods=['POST'])
@login_required
def update():
    if Tweet.check_token():
        form = request.form
        Tweet.check_id(form)
        Tweet.update(form)
        # todo Tweet update 完成之后 需要到 Tweet 的 index 页面 还是 detail 页面呢？
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
    return render_template('tweet/tweet_detail.html', t=t, user=user)


@main.route('/like/<int:tweet_id>', methods=['GET'])
@login_required
def like(tweet_id):
    user = current_user()
    t = Tweet.find(tweet_id)
    if Tweet.check_token():
        t.like(user.id)
        user.like_tweet(tweet_id)
        return redirect(url_for('.detail', tweet_id=tweet_id, token=gg.token[user.id]))


@main.route('/delike/<int:tweet_id>', methods=['GET'])
@login_required
def delike(tweet_id):
    user = current_user()
    t = Tweet.find(tweet_id)
    if Tweet.check_token():
        t.delike(user.id)
        user.delike_tweet(tweet_id)
        return redirect(url_for('.detail', tweet_id=tweet_id, token=gg.token[user.id]))
