secret_key = 'Be the greatest，or nothing'
import os
import os.path
image_file_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/image')
accept_image_file_type = ['jpg', 'gif', 'png']

# print(image_file_dir)
# /Users/caiwei/PycharmProjects/PythonWeb/server_normal_Flask/image


# 此处用七牛云SDK存图片，user的user_name存图片名
def qiniu_up(pic_name):
    from qiniu import Auth, put_file, etag, urlsafe_base64_encode
    import qiniu.config

    # 需要填写你的 Access Key 和 Secret Key
    access_key = '3WdBnUyD1kJmJEg9Tih3fzmcGoxYFUGBO9RtKJN7'
    secret_key = 'dFL1xftxFoTPSXUCc1tg3g9Ve0DafpHKsWABCmhg'

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的空间
    bucket_name = 'python-web'

    # 上传到七牛后保存的文件名
    key = pic_name

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    localfile = os.path.join(image_file_dir, pic_name)

    ret, info = put_file(token, key, localfile)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)
    # 返回外链domain
    return 'http://p5shjfo1t.bkt.clouddn.com/'


# 图片格式安全过滤
def allow_file(filename):
    suffix = filename.split('.')[-1]
    return suffix in accept_image_file_type


def check_image(file):
    if allow_file(file.filename):
        from werkzeug.utils import secure_filename
        # 上传的文件一定要用 secure_filename 函数过滤一下名字
        # ../../../../../../../root/.ssh/authorized_keys
        filename = secure_filename(file.filename)
        # 2018/3/19/yiasduifhy289389f.png
        file.save(os.path.join(image_file_dir, filename))
        # u.add_avatar(filename)
        domain = qiniu_up(filename)
        os.remove(os.path.join(image_file_dir, filename))
        user_image = domain + filename
        return user_image

import uuid
class global_token(object):
    def __init__(self):
        self.csrf_tokens = dict()
        self.token = ''

    def get_value(self):
        return self.csrf_tokens, self.token

    def set_value(self, user_id):
        self.token = str(uuid.uuid4())
        self.csrf_tokens[self.token] = user_id

    def delete_value(self):
        # 空字典不能pop
        if self.token != '':
            self.csrf_tokens.pop(self.token)

    def reset_value(self, user_id):
        self.delete_value()
        self.set_value(user_id)


gg = global_token()

print('from config',gg.csrf_tokens, gg.token)
