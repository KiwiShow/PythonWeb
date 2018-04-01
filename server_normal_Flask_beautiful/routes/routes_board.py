from utils import log
from routes import (
    current_user,
    login_required,
)

from flask import (
    request,
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    make_response,
    send_from_directory,
)
from models.board import Board
from models.user import User
from config import  gg


main = Blueprint('board', __name__)


@main.route('/add', methods=['POST'])
@login_required
def add():
    token = request.args.get('token')
    if Board.check_token(token, gg.csrf_tokens):
        User.check_admin()
        form = request.form
        b = Board.new(form)
        return redirect(url_for('user.admin', token=token))


@main.route('/delete/<int:board_id>')
@login_required
def delete(board_id):
    token = request.args.get('token')
    if Board.check_token(token, gg.csrf_tokens):
        User.check_admin()
        Board.remove(board_id)
        return redirect(url_for('user.admin', token=token))


@main.route('/edit/<int:board_id>', methods=['GET'])
@login_required
def edit(board_id):
    """
    只有用户id为1的用户有权限，输入需要修改的id和password
    :return: 返回修改过的所有用户的信息
    """
    user = current_user()
    token = request.args.get('token')
    if User.check_token(token, gg.csrf_tokens):
        User.check_admin()
        b = Board.find(board_id)
        return render_template('board/board_edit.html', token=token, user=user, b=b)


@main.route('/update', methods=['POST'])
@login_required
def update():
    token = request.args.get('token')
    if Board.check_token(token, gg.csrf_tokens):
        User.check_admin()
        form = request.form
        Board.update(form)
        # redirect有必要加query吗
        return redirect(url_for('user.admin', token=token))
