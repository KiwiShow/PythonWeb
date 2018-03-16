class HashTable(object):
    def __init__(self):
        self.table_size = 101
        self.table = [0] * self.table_size

    # 这个魔法方法是用来实现 in  not in 语法的
    def __contains__(self, item):
        return self.has_key(item)

    def _index(self, key):
        return self._hash(key) % self.table_size

    def _hash(self, s):
        n = 1
        f = 1
        for i in s:
            n += ord(i) * f
            f *= 10
        return n

    def _insert_at_index(self, index, key, value):
        v = self.table[index]
        data = [key, value]
        if isinstance(v, int):
            self.table[index] = [data]
        else:
            # 这里有key完全一样的问题
            self.table[index].append([data])

    def add(self, key, value):
        index = self._index(key)
        self._insert_at_index(index, key, value)

    # has_key和get几乎一样
    def has_key(self, key):
        index = self._index(key)
        v = self.table[index]
        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    return True
        return False

    def get(self, key, default_value=None):
        index = self._index(key)
        v = self.table[index]
        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    return kv[1]
        return default_value


def test():
    import uuid
    names = [
        'kiwi',
        'name',
        'web',
        'python',
    ]
    ht = HashTable()
    for key in names:
        value = uuid.uuid4()
        ht.add(key, value)
        print('add 元素', key, value, ht.table)
    for key in names:
        v = ht.get(key)
        print('get 元素', key, v, ht.table)


if __name__ == '__main__':
    test()
