from flask import (
    request,
    Blueprint,
    render_template,
)

main = Blueprint('error', __name__)


@main.app_errorhandler(401)
def forbidden(e):
    return render_template('error/401.html'), 401


@main.app_errorhandler(403)
def forbidden(e):
    return render_template('error/403.html'), 403


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


# @main.app_errorhandler(500)
# def internal_server_error(e):
#     if request.accept_mimetypes.accept_json and \
#             not request.accept_mimetypes.accept_html:
#         response = jsonify({'error': 'internal server error'})
#         response.status_code = 500
#         return response
#     return render_template('500.html'), 500
