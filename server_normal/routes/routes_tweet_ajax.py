from models.user import User
from models.tweet import Tweet
from models.comment import Comment

from session import session

from utils import log, template, json_response

from routes import (
    redirect,
    http_response,
    error,
    login_required,
    check_id,
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



# def delete(request):
#     u = current_user(request)
#     tweet_id = int(request.query.get('id'))
#     t = Tweet.find(tweet_id)
#     if u.id == t.user_id:
#         t.remove(tweet_id)
#     # redirect有必要加query吗
#     return redirect('/tweet/index?user_id={}'.format(u.id))
#
#
# def new(request):
#     body = template('tweet_new.html')
#     return http_response(body)
#
#
# def add(request):
#     u = current_user(request)
#     form = request.form()
#     t = Tweet.new(form, user_id=u.id)
#     # t.user_id = u.id
#     # t.save()
#     # redirect有必要加query吗
#     return redirect('/tweet/index?user_id={}'.format(u.id))
#
#
# def edit(request):
#     tweet_id = request.query.get('id', -1)
#     tweet_id = int(tweet_id)
#     t = Tweet.find(tweet_id)
#     if t is None:
#         return error(request)
#     body = template('tweet_edit.html',
#                     tweet_id=t.id,
#                     tweet_content=t.content)
#     return http_response(body)
#
#
# def update(request):
#     u = current_user(request)
#     form = request.form()
#     content = form.get('content', '')
#     tweet_id = int(form.get('id', -1))
#     t = Tweet.find(tweet_id)
#     if u.id != t.user_id:
#         return error(request)
#     t.content = content
#     t.save()
#     # redirect有必要加query吗
#     return redirect('/tweet/index?user_id={}'.format(u.id))
#
#
# def comment_add(request):
#     user = current_user(request)
#     form = request.form()
#     c = Comment.new(form, user_id=user.id)
#     # c.save()
#     uid = c.tweet().user().id
#     return redirect('/tweet/index?user_id={}'.format(uid))
#
#
# def comment_delete(request):
#     u = current_user(request)
#     comment_id = request.query.get('id', -1)
#     comment_id = int(comment_id)
#     c = Comment.find(comment_id)
#     if u.id == c.user_id:
#         c.remove(comment_id)
#     return redirect('/tweet/index?user_id={}'.format(u.id))


route_dict = {
    '/ajax/tweet/index': login_required(index),
    '/ajax/comment/index': login_required(comment_index),
    # '/tweet/delete': login_required(delete),
    # '/tweet/edit': login_required(edit),
    # '/tweet/update': login_required(update),
    # '/tweet/add': login_required(add),
    # '/tweet/new': login_required(new),
    # # 评论功能
    # '/comment/add': login_required(comment_add),
    # '/comment/delete': login_required(comment_delete),
}
