# 1. remove ，删除元素
# 2. add， 增加元素
# 3. has，判断元素是否存在


class OriHashTable(object):
    def __init__(self, **kwargs):
        self.size = 101
        self.data = [None] * self.size

        for k, v in kwargs.items():
            self.add(k, v)

    def index(self, key):
        # hash 是 python 内置的函数，可以获得一个数字
        i = hash(key) % self.size
        return i

    def remove(self, key):
        index = self.index(key)
        data = self.data
        kvs = data[index]
        if kvs is None:
            # // 如果 kvs 是 None 说明这个下标还没存储过数据
            # // 那么就要让它初始化为一个数组
            data[index] = []
        elif isinstance(kvs, list):
            # 如果kvs 是队列，需要遍历 kvs 查看是否存储了数据在里面
            for kv in kvs:
                if kv[0] == key:
                    kvs.remove(kv)

    def add(self, key, value):
        index = self.index(key)
        data = self.data
        kvs = data[index]
        if kvs is None:
            # // 如果 kvs 是 None 说明这个下标还没存储过数据
            # // 那么就要让它初始化为一个数组
            data[index] = [(key, value)]
        elif isinstance(kvs, list):
            # 如果kvs 是队列，需要遍历 kvs 查看是否存储了数据在里面
            # 先找index一样，再找key完全一样
            for kv in kvs:
                if kv[0] == key:
                    kv[1] = value
                    break

    def has(self, key):
        index = self.index(key)
        data = self.data
        kvs = data[index]
        if kvs is None:
            # // 如果 kvs 是 None 说明这个下标还没存储过数据
            # // 那么就要让它初始化为一个数组
            data[index] = []
        elif isinstance(kvs, list):
            # 如果kvs 是队列，需要遍历 kvs 查看是否存储了数据在里面
            for kv in kvs:
                if kv[0] == key:
                    return True
        return False


# 在OriHashTable类里增加 __repr__  和 __eq__ 两个成员函数。
# 并且实现了代码复用cursor
class HashTable(object):
    def __init__(self):
        self.size = 101
        self.data = [None] * self.size
        # 初始化所有cell 都是 None

    def index(self, key):
        # hash 是 python 内置的函数，可以获得一个数字
        i = hash(key) % self.size
        return i

    def __repr__(self):
        ds = [str(x) for x in self.items()]
        s = ', '.join(ds)
        m = '< %s >' % s
        return m

    def __eq__(self, other):
        # 比较两个对象是否相等
        for item in self.items():
            k, v = item
            dv = other.get(k)
            if v != dv:
                return False
        return True

    def keys(self):
        # 所有键值
        ks = [kv[0] for kv in self.items()]
        return ks

    def items(self):
        # 返回迭代对象，这个函数用于比较两个对象是否相等。
        for kvs in self.data:
            if isinstance(kvs, list):
                for kv in kvs:
                    yield kv

    def cursor(self, key):
        index = self.index(key)
        data = self.data
        kvs = data[index]
        if kvs is None:
            # 如果 kvs 是 None 说明这个下标还没存储过数据
            # 那么就要让它初始化为一个数组
            # 这样做的好处是，能统一其它操作。
            # 该index后续直接走elif
            data[index] = []
            return None
        elif isinstance(kvs, list):
            # 如果kvs 是队列，需要遍历 kvs 查看是否存储了数据在里面
            # for i in range(len(kvs)):
            for i, kv in enumerate(kvs):
                # 配合for i in range(len(kvs)):使用
                # kv = kvs[i]
                if kv[0] == key:
                    # 设想index(key)代表x轴，i代表y轴，kv代表某一点
                    # 返回点命中结果
                    return index, i, kv
                # 返回面命中结果
                return index, 'many', kvs

    # 查1
    def has(self, key):
        cursor = self.cursor(key)
        return cursor is not None

    # 查2
    def get(self, key, default=None):
        cursor = self.cursor(key)
        if cursor is None:
            return default
        else:
            index, i, kv = cursor
            return kv[1]

    # 删
    def remove(self, key):
        cursor = self.cursor(key)
        if cursor is not None:
            index, i, kv = cursor
            value = kv[1]
            self.data[index].remove(kv)
            return value

    # 增 and update
    def add(self, key, value):
        cursor = self.cursor(key)
        if cursor is None:
            index = self.index(key)
            # 在cursor执行完None变成[]
            self.data[index].append((key, value))
        else:
            index, i, kv = cursor
            new_kv = (key, value)
            if i == 'many':
                self.data[index].append(new_kv)
            else:
                # 等于update
                self.data[index][i] = new_kv


def test_hash_table():
    a = HashTable()
    a.add('apple', 'mac')
    # 瑜伽key一样时，add相当于update
    # a.add('apple', 'macnew')
    a.add('coder', 'js')
    print(a)
    assert a.has('apple')
    assert not a.has('pie')
    assert a.get('apple') == 'mac'
    assert a.get('pie') is None
    # a.add('apple', 'tree')
    # print(a)
    print(a.add('apple', 'tree'))
    assert a.get('apple') == 'tree'
    assert a.remove('apple') == 'tree'
    assert a.remove('apple') is None

    print(a, a.items(), a.keys())

    b = HashTable()
    b.add('coder', 'js')
    print(b)
    for i in range(10):
        a.add(i, str(i))
        b.add(i, str(i))
    print(a == b)
    assert a == b
    print(a)
    print(b)


if __name__ == '__main__':
    test_hash_table()
