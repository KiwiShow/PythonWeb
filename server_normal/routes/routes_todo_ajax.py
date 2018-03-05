from utils import log, template, json_response
from routes import (
    redirect,
    response_with_headers,
    login_required,
    current_user,
)
from models.to_be_mongo import change_time
from models.todo import Todo
import time


def index(request):
    u = current_user(request)
    todos = Todo.find_all_json(user_id=u.id, deleted=False)
    return json_response(todos)


route_dict = {
    '/ajax/todo/index': login_required(index),
}
