from models.user import User
from models.tweet import Tweet
from models.comment import Comment

from session import session

from utils import log, template

from routes import (
    redirect,
    http_response,
    error,
)
from routes.routes_user import current_user
from routes.routes_todo import login_required


def index(request):
    # 从query取到user_id可以到该用户界面评论
    user_id = int(request.query.get('user_id', -1))
    if user_id == -1:
        u = current_user(request)
        user_id = u.id
    user = User.find(user_id)
    if user is None:
        return redirect('/login')
    else:
        tweets = Tweet.find_all(user_id=user.id, deleted=False)
        body = template('tweet_index.html', tweets=tweets, user=user)
        return http_response(body)


def delete(request):
    u = current_user(request)
    tweet_id = int(request.query.get('id'))
    t = Tweet.find(tweet_id)
    if u.id == t.user_id:
        # 这里只是删除了tweet，但是其所拥有的comment的deleted字段变成False
        t.remove(tweet_id)
        for c in t.comments():
            c.deleted = True
            c.save()
    # redirect有必要加query吗
    return redirect('/tweet/index?user_id={}'.format(u.id))


def new(request):
    body = template('tweet_new.html')
    return http_response(body)


def add(request):
    u = current_user(request)
    form = request.form()
    t = Tweet.new(form, user_id=u.id)
    # t.user_id = u.id
    # t.save()
    # redirect有必要加query吗
    return redirect('/tweet/index?user_id={}'.format(u.id))


def edit(request):
    tweet_id = request.query.get('id', -1)
    tweet_id = int(tweet_id)
    t = Tweet.find(tweet_id)
    if t is None:
        return error(request)
    body = template('tweet_edit.html',
                    tweet_id=t.id,
                    tweet_content=t.content)
    return http_response(body)


def update(request):
    u = current_user(request)
    form = request.form()
    content = form.get('content', '')
    tweet_id = int(form.get('id', -1))
    t = Tweet.find(tweet_id)
    if u.id != t.user_id:
        return error(request)
    t.content = content
    t.save()
    # redirect有必要加query吗
    return redirect('/tweet/index?user_id={}'.format(u.id))


def comment_add(request):
    user = current_user(request)
    form = request.form()
    c = Comment.new(form, user_id=user.id)
    # c.save()
    uid = c.tweet().user().id
    return redirect('/tweet/index?user_id={}'.format(uid))


def comment_delete(request):
    u = current_user(request)
    comment_id = request.query.get('id', -1)
    comment_id = int(comment_id)
    c = Comment.find(comment_id)
    if u.id == c.user_id:
        c.remove(comment_id)
    return redirect('/tweet/index?user_id={}'.format(u.id))


route_dict = {
    '/tweet/index': login_required(index),
    '/tweet/delete': login_required(delete),
    '/tweet/edit': login_required(edit),
    '/tweet/update': login_required(update),
    '/tweet/add': login_required(add),
    '/tweet/new': login_required(new),
    # 评论功能
    '/comment/add': login_required(comment_add),
    '/comment/delete': login_required(comment_delete),
}
