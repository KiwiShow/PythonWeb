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


main = Blueprint('board', __name__)


@main.route('/add', methods=['POST'])
@login_required
def add():
    form = request.form
    b = Board.new(form)
    return redirect(url_for('user.admin'))


@main.route('/delete/<int:board_id>')
@login_required
def delete(board_id):
    Board.remove(board_id)
    return redirect(url_for('user.admin'))


@main.route('/update', methods=['POST'])
@login_required
def update():
        form = request.form
        Board.update(form)
        # redirect有必要加query吗
        return redirect(url_for('user.admin'))
