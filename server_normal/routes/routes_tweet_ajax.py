from models.user import User
from models.tweet import Tweet
from models.comment import Comment

from session import session

from utils import log, template, json_response

from routes import (
    http_response,
    error,
    login_required,
    check_id_tweet,
    check_id_comment,
)
from routes.routes_user import current_user


def index(request):
    # 从query取到user_id可以到该用户界面评论
    user_id = int(request.query.get('user_id', -1))
    if user_id == -1:
        u = current_user(request)
        user_id = u.id
    user = User.find(user_id)
    tweets = Tweet.find_all_json(user_id=user.id, deleted=False)
    return json_response(tweets)


def comment_index(request):
    tweet_id = int(request.query.get('tweet_id'))
    comments = Comment.find_all_json(tweet_id=tweet_id, deleted=False)
    return json_response(comments)


def add(request):
    user = current_user(request)
    form = request.json()
    t = Tweet.new(form, user_id=user.id, user_name=user.username)
    return json_response(t.json())


def delete(request):
    tweet_id = int(request.query.get('id'))
    t = Tweet.find_by(id=tweet_id)
    check_id_tweet(request, id=tweet_id)
    Tweet.remove(tweet_id)
    # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
    return json_response(t.json())


def update(request):
    form = request.json()
    check_id_tweet(request, form)
    newTweet = Tweet.update(form)
    return json_response(newTweet.json())



def comment_add(request):
    user = current_user(request)
    form = request.json()
    c = Comment.new(form, user_id=user.id, user_name=user.username)
    # uid = c.tweet().user().id
    return json_response(c.json())


def comment_delete(request):
    comment_id = int(request.query.get('id'))
    t = Comment.find_by(id=comment_id)
    check_id_comment(request, id=comment_id)
    Comment.remove(comment_id)
    # 不管如何，都需要返回json的数据，为了触发ajax中回调函数
    return json_response(t.json())


def comment_update(request):
    form = request.json()
    check_id_comment(request, form)
    newComment = Comment.update(form)
    return json_response(newComment.json())

route_dict = {
    '/ajax/tweet/index': login_required(index),
    '/ajax/tweet/add': login_required(add),
    '/ajax/tweet/delete': login_required(delete),
    '/ajax/tweet/update': login_required(update),
    # 评论功能
    '/ajax/comment/index': login_required(comment_index),
    '/ajax/comment/add': login_required(comment_add),
    '/ajax/comment/delete': login_required(comment_delete),
    '/ajax/comment/update': login_required(comment_update),
}
