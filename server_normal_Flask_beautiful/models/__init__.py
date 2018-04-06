from utils import log
import time
from pymongo import MongoClient
from flask import abort, request
from config import gg


mon = MongoClient('mongodb://localhost:27017')


def change_time(t):
    format = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(t)
    dt = time.strftime(format, value)
    return dt


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = mon.web_flask_beautiful['data_id']
    # 这里有个小问题：data_id表里的seq是一直增加的，所以其它类型数据的id是一直增加的，不存在其它类型
    # 的表删除之后id从0开始
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class MonModel(object):
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    @classmethod
    def new(cls, form=None, **kwargs):  # new完已经保存了一次
        name = cls.__name__
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        if form is None:
            form = {}
        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        m.id = next_id(name)
        t = int(time.time())
        # 因为需要算基于linux时间算delta，所以不需要格式化时间
        # m.created_time = change_time(t)
        # m.updated_time = change_time(t)
        m.created_time = t
        m.updated_time = t
        m.type = name.lower()
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def all(cls):
        return cls._find()

    # 找到类所有的实例,返回json类型数据
    @classmethod
    def all_json(cls):
        ms = cls.all()
        jsons = [m.json() for m in ms]
        return jsons

    @classmethod
    def _find(cls, **kwargs):
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        # 这里 kwargs 没有对 deleted 做出限定，所以已删除的 还会 被找到
        # 所以需要对 deleted=False 做出限定，避免在子类的路由函数中增加 deleted=False
        # if 'deleted' not in kwargs.keys():
        #     dd = {
        #         'deleted': False,
        #     }
        #     kwargs.update(dd)

        dd = {
            'deleted': False,
        }
        kwargs.update(dd)
        ds = mon.web_flask_beautiful[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    # 找到类所有满足条件的实例，返回json类型数据
    @classmethod
    def find_all_json(cls, **kwargs):
        ms = cls.find_all(**kwargs)
        jsons = [m.json() for m in ms]
        return jsons

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    # **kwargs 针对mail一方删除，另外一方还可以看
    @classmethod
    def remove(cls, id, **kwargs):
        name = cls.__name__
        query = {
            'id': id,
        }
        values = {
            'deleted': True
        }
        if 'sender_deleted' in kwargs.keys() or 'receiver_deleted' in kwargs.keys():
            values = kwargs
        mon.web_flask_beautiful[name].update_one(query, {"$set": values})

    # whitelist 是一个列表， query 和 form 都是 字典
    @classmethod
    def ori_update(cls, whitelist, id, form, password=None):
        name = cls.__name__
        query = {
            'id': id,
        }
        values = {}
        for key in whitelist:
            if form.get(key, '') != '':
                values[key] = form.get(key)
        tm = int(time.time())
        values.pop('id')
        if password:
            values['password'] = password
        values['updated_time'] = tm
        # print('value', values)
        mon.web_flask_beautiful[name].update_one(query, {"$set": values})

    def save(self):
        name = self.__class__.__name__
        mon.web_flask_beautiful[name].save(self.__dict__)

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    # def json(self):
    #     """
    #     返回当前 model 的字典表示
    #     """
    #     # copy 会复制一份新数据并返回
    #     d = self.__dict__.copy()
    #     return d

    def __repr__(self):
        """
        这是一个 魔法函数
        不明白就看书或者 搜
        u = User.new({})
        print(u)
        实际上 相当于 print(repr(u))
        实际上 相当于 print(u.__repr__())
        """
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    @classmethod
    def check_id(cls, form=None, id=None):
        if id == None:
            m_id = int(form.get('id', -1))
        else:
            m_id = id
        m = cls.find_by(id=m_id)
        from routes import current_user
        from flask import redirect, url_for
        u = current_user()
        if u.id != m.user_id:
            return redirect(url_for('.login'))

    @classmethod
    def check_token(cls):
        from routes import current_user
        token = request.args.get('token')
        user = current_user()
        if gg.csrf_tokens[token] == user.id:
            return True
        else:
            abort(403)



    # todo 暂时不用
    def data_count(self, cls):
        """
        神奇的函数, 查看用户发表的评论数
        u.data_count(Comment)
        :return: int
        """
        name = cls.__name__
        # TODO, 这里应该用 type 替代
        fk = '{}_id'.format(self.__class__.__name__.lower())
        query = {
            fk: self.id,
        }
        count = mon.web_flask_beautiful[name]._find(query).count()
        return count

# # Model 是用于存储数据的基类
# class Model(object):
#     # @classmethod 说明这是一个 类方法
#     # 类方法的调用方式是  类名.类方法()
#     @classmethod
#     def db_path(cls):
#         # classmethod 有一个参数是 class
#         # 所以我们可以得到 class 的名字
#         classname = cls.__name__
#         path = 'db/{}.txt'.format(classname)
#         return path
#
#     @classmethod
#     def new(cls, form):
#         m = cls(form)
#         # cls(form) 相当于 User(form)
#         return m
#
#     @classmethod
#     def all(cls):
#         """
#         得到一个类的所有存储的实例
#         """
#         path = cls.db_path()
#         models = load(path)
#         # 此时models还只是一个列表
#         # m只是一个字典还不是对象，所以需要cls.new(m)一下变为User 或者 Message 对象
#         ms = [cls.new(m) for m in models]
#         return ms
#
#     # 为 Model 添加一个类方法 find_by
#     # 用法和例子如下
#     """
#     u = User.find_by(username='dog')
#
#     上面这句可以返回一个 username 属性为 'dog' 的 User 实例
#     如果有多条这样的数据, 返回第一个
#     如果没这样的数据, 返回 None
#
#     注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
#     但是现在这个方法只有一个参数
#     """
#
#     # Model.find_by(a=b, c=d) => Model.find_by(c=d)
#     @classmethod
#     def find_by(cls, **kwargs):
#         all = cls.all()
#         k, v = '', ''
#         # 其实也只能找到一个
#         for key, value in kwargs.items():
#             k, v = key, value
#         for one in all:
#             if v == one.__dict__[k]:
#                 return one
#         return None
#
#     @classmethod
#     def find_all(cls, **kwargs):
#         all = cls.all()
#         k, v = '', ''
#         for key, value in kwargs.items():
#             k, v = key, value
#         result = []
#         for one in all:
#             # getattr(m, k) === v
#             if v == one.__dict__[k]:
#                 result.append(one)
#         # 若一个都没找到，那么返回[]
#         return result
#
#     @classmethod
#     def find(cls, id):
#         return cls.find_by(id=id)
#
#     @classmethod
#     def remove(cls, id):  # id 必须是int
#         ms = cls.all()
#         index = -1
#         for i, m in enumerate(ms):
#             if m.id == id:
#                 index = i
#                 break
#         if index > -1:
#             del ms[index]
#         # 为什么有以下语句，因为save的参数需要dict或者元素是dict的list
#         l = [m.__dict__ for m in ms]
#         path = cls.db_path()
#         save(l, path)
#
#     def check_id(self, models):
#         if self.id is None:
#             if len(models) > 0:
#                 self.id = models[-1].id + 1
#             else:
#                 self.id = 1
#             models.append(self)
#         else:
#             index = -1
#             for i, m in enumerate(models):
#                 if m.id == self.id:
#                     index = i
#                     break
#             if index > -1:
#                 models[index] = self
#         return models
#
#     def save(self):
#         """
#         save 函数用于把一个 Model 的实例保存到文件中
#         """
#         models = self.all()
#         # log('models', models)
#
#         # 这里验证id
#         models = self.check_id(models)
#
#         # models.append(self)
#         # __dict__ 是包含了对象所有属性和值的字典
#         # 你要的不是一个每个元素为对象的列表，而是每个元素为字典的列表 from kiwi
#         l = [m.__dict__ for m in models]
#         path = self.db_path()
#         save(l, path)
#
#     def __repr__(self):
#         """
#         这是一个 魔法函数
#         不明白就看书或者 搜
#         u = User.new({})
#         print(u)
#         实际上 相当于 print(repr(u))
#         实际上 相当于 print(u.__repr__())
#         """
#         classname = self.__class__.__name__
#         properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
#         s = '\n'.join(properties)
#         return '< {}\n{} >\n'.format(classname, s)
