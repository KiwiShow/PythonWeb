from utils import log
from models.mail import Mail
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


main = Blueprint('mail', __name__)


# mail是私人的，只有自己可以看
@main.route('/index', methods=['GET'])
@login_required
def index():
    """
    显示该用户所有mail
    :return: 显示mail页面
    """
    user = current_user()
    if user is not None:
        gg.delete_value()
        gg.set_value(user.id)
        log('from mail',gg.csrf_tokens, gg.token)
        send_mail = Mail.find_all(sender_id=user.id)
        received_mail = Mail.find_all(receiver_id=user.id)
        return render_template('mail/mail_index.html', sends=send_mail, receives=received_mail, token=gg.token, user=user)


@main.route('/new/<int:to_user_id>', methods=['GET'])
@login_required
def new(to_user_id):
    user = current_user()
    token = request.args.get('token')
    if Mail.check_token(token, gg.csrf_tokens):
        return render_template('mail/mail_new.html', token=token, to_user_id=to_user_id, user=user)


@main.route('/add', methods=['POST'])
@login_required
def add():
    token = request.args.get('token')
    if Mail.check_token(token, gg.csrf_tokens):
        form = request.form
        # form里面有title，content，sender_id，receiver_id
        m = Mail.new(form)
        return redirect(url_for('.index'))


@main.route('/delete/<int:mail_id>', methods=['GET'])
@login_required
def delete(mail_id):
    # mail_id = int(request.args.get('id'))
    token = request.args.get('token')
    if Mail.check_token(token, gg.csrf_tokens):
        # gg.delete_value()
        # csrf_tokens.pop(token)
        m = Mail.find(mail_id)
        # check_id 需要 user_id 而 mail类 没有
        # Mail.check_id(id=mail_id)
        if current_user().id in [m.receiver_id, m.sender_id]:
            m.remove(mail_id)
            return redirect(url_for('.index'))


@main.route('/edit/<int:mail_id>', methods=['GET'])
@login_required
def edit(mail_id):
    user = current_user()
    token = request.args.get('token')
    if Mail.check_token(token, gg.csrf_tokens):
    # mail_id = int(request.args.get('id', -1))
        m = Mail.find(mail_id)
        if current_user().id in [m.receiver_id, m.sender_id]:
            return render_template('mail/mail_edit.html', m=m, token=token, user=user)


@main.route('/update/<int:mail_id>', methods=['POST'])
@login_required
def update(mail_id):
    token = request.args.get('token')
    if Mail.check_token(token, gg.csrf_tokens):
        form = request.form
        m = Mail.find(mail_id)
        if current_user().id in [m.receiver_id, m.sender_id]:
            Mail.update(form)
            # redirect有必要加query吗
            return redirect(url_for('.index'))


@main.route('/detail/<int:mail_id>', methods=['GET'])
@login_required
def detail(mail_id):
    user = current_user()
    m = Mail.mark_read(mail_id)
    token = request.args.get('token')
    return render_template('mail/mail_detail.html', m=m, token=token, user=user)
