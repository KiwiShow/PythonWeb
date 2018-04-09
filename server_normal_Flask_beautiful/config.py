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

# token的位置
# 1.header
# 2.url
# 3.body
# token 应该是 每个 页面 都有 一个新的 token，这个页面上的所有操作都需要此token 验证
import uuid
class global_token(object):
    def __init__(self):
        # 分别以 token  和  user_id  为 key
        self.csrf_tokens = dict(test_token=4)
        self.token = dict()

    def get_value(self):
        return self.csrf_tokens, self.token

    def set_value(self, user_id):
        uu = str(uuid.uuid4())
        self.csrf_tokens[uu] = user_id
        self.token[user_id] = uu

    def delete_value(self, user_id):
        # 空字典不能pop
        # 出现的问题，一个用户登录之后，另一个用户登录会清空 gg.csrf_tokens
        # from tweet  before
        # {}
        # from tweet  after
        # {'06cf4caa-545a-47c3-be9f-f26b58662918': 1}
        # 06cf4caa-545a-47c3-be9f-f26b58662918
        # from tweet  before
        # {'06cf4caa-545a-47c3-be9f-f26b58662918': 1}
        # 06cf4caa-545a-47c3-be9f-f26b58662918
        # from tweet  after
        # {'3400079f-f74a-42db-ad61-9248bab54bef': 2}
        # 3400079f-f74a-42db-ad61-9248bab54bef
        t = self.token.get(user_id, '')
        if t != '':
            self.csrf_tokens.pop(t)
            self.token.pop(user_id)

    def reset_value(self, user_id):
        self.delete_value(user_id)
        self.set_value(user_id)


gg = global_token()

print('from config',gg.csrf_tokens, gg.token)
