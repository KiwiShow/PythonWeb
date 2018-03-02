import json

from utils import log


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    # json 是一个序列化/反序列化list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    # dumps: 对象 --> 列表 --> 字符串
    # dumps的参数data是列表的格式，所以dumps负责列表 --> 字符串这一段，而对象 --> 列表由l = [m.__dict__ for m in models]负责。
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        # log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        # log('load', s)
        # loads: 相反，字符串 --> 列表 --> 对象。
        # loads的参数是字符串的格式，所以loads负责字符串 --> 列表这一段，而 列表 --> 对象由ms = [cls.new(m) for m in models]负责。
        return json.loads(s)


# Model 是用于存储数据的基类
class Model(object):
    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        # cls(form) 相当于 User(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        # 此时models还只是一个列表
        # m只是一个字典还不是对象，所以需要cls.new(m)一下变为User 或者 Message 对象
        ms = [cls.new(m) for m in models]
        return ms

    # 为 Model 添加一个类方法 find_by
    # 用法和例子如下
    """
    u = User.find_by(username='dog')
    
    上面这句可以返回一个 username 属性为 'dog' 的 User 实例
    如果有多条这样的数据, 返回第一个
    如果没这样的数据, 返回 None
    
    注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
    但是现在这个方法只有一个参数
    """

    # Model.find_by(a=b, c=d) => Model.find_by(c=d)
    @classmethod
    def find_by(cls, **kwargs):
        all = cls.all()
        k, v = '', ''
        # 其实也只能找到一个
        for key, value in kwargs.items():
            k, v = key, value
        for one in all:
            if v == one.__dict__[k]:
                return one
        return None

    @classmethod
    def find_all(cls, **kwargs):
        all = cls.all()
        k, v = '', ''
        for key, value in kwargs.items():
            k, v = key, value
        result = []
        for one in all:
            # getattr(m, k) === v
            if v == one.__dict__[k]:
                result.append(one)
        # 若一个都没找到，那么返回[]
        return result

    @classmethod
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod
    def remove(cls, id):  # id 必须是int
        ms = cls.all()
        index = -1
        for i, m in enumerate(ms):
            if m.id == id:
                index = i
                break
        if index > -1:
            del ms[index]
        # 为什么有以下语句，因为save的参数需要dict或者元素是dict的list
        l = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(l, path)

    def check_id(self, models):
        if self.id is None:
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                self.id = 1
            models.append(self)
        else:
            index = -1
            for i, m in enumerate(models):
                if m.id == self.id:
                    index = i
                    break
            if index > -1:
                models[index] = self
        return models

    def save(self):
        """
        save 函数用于把一个 Model 的实例保存到文件中
        """
        models = self.all()
        # log('models', models)

        # 这里验证id
        models = self.check_id(models)

        # models.append(self)
        # __dict__ 是包含了对象所有属性和值的字典
        # 你要的不是一个每个元素为对象的列表，而是每个元素为字典的列表 from kiwi
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

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
