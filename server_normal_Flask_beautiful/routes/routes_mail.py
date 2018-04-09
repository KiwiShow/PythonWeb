from utils import log
from models.mail import Mail
from models.user import User
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
        print('from mail  before', gg.csrf_tokens)
        gg.reset_value(user.id)
        print('from mail  after', gg.csrf_tokens)

        send_mail = Mail.find_all(sender_id=user.id, sender_deleted=False)
        received_mail = Mail.find_all(receiver_id=user.id, receiver_deleted=False)
        return render_template('mail/mail_index.html', sends=send_mail, receives=received_mail, token=gg.token[user.id], user=user)


@main.route('/new/<int:to_user_id>', methods=['GET'])
@login_required
def new(to_user_id):
    user = current_user()
    if Mail.check_token():
        return render_template('mail/mail_new.html', token=gg.token[user.id], to_user_id=to_user_id, user=user)


@main.route('/add', methods=['POST'])
@login_required
def add():
    if Mail.check_token():
        form = request.form
        # form里面有title，content，sender_id，receiver_id
        m = Mail.new(form)
        # 管理员 回到管理员 界面
        if current_user().id == 1:
            return redirect(url_for('.index', token=gg.token[current_user().id]))
        return redirect(url_for('.index'))


# 群发私信
@main.route('/admin_add', methods=['POST'])
@login_required
def admin_add():
    if Mail.check_token():
        User.check_admin()
        form = request.form
        for u in User.find_all():
            if u.id != 1:
                m = Mail.new(form, receiver_id=u.id)
        return redirect(url_for('user.admin', token=gg.token[current_user().id]))


@main.route('/delete/<int:mail_id>', methods=['GET'])
@login_required
def delete(mail_id):
    if Mail.check_token():
        Mail.receiver_sender_delete(mail_id)
        return redirect(url_for('.index'))


@main.route('/edit/<int:mail_id>', methods=['GET'])
@login_required
def edit(mail_id):
    user = current_user()
    if Mail.check_token():
    # mail_id = int(request.args.get('id', -1))
        m = Mail.find(mail_id)
        if current_user().id in [m.receiver_id, m.sender_id]:
            return render_template('mail/mail_edit.html', m=m, token=gg.token[user.id], user=user)


@main.route('/update/<int:mail_id>', methods=['POST'])
@login_required
def update(mail_id):
    if Mail.check_token():
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
    return render_template('mail/mail_detail.html', m=m, token=gg.token[user.id], user=user)
