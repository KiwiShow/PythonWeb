# 一个 Set 的类, 无序且元素不重复，内部使用数组来存储元素
class Set(object):
    def __init__(self, *args):
        self.data = []
        for x in args:
            self.add(x)

    def __repr__(self):
        ds = [str(x) for x in self.data]
        s = ', '.join(ds)
        m = '{' + '{}'.format(s) + '}'
        return m

    def __eq__(self, other):
        for x in self.data:
            if not other.has(x):
                return False
        return True

    # O(n)
    def remove(self, x):
        self.data.remove(x)

    # O(n)
    def add(self, x):
        if not self.has(x):
            self.data.append(x)

    # O(n)
    def has(self, x):
        return x in self.data


def testSet():
    a = Set(1, 2, 2, 3, 4, 4)
    b = Set(1, 2, 2, 3, 4)
    c = Set(1, 3, 4, 2)
    d = Set(2, 3)
    print (str(a))
    assert (str(a) == '{1, 2, 3, 4}')
    print(a, b, c, d)
    assert (a == b)
    assert (a == c)
    assert (a != d)
    assert (a.has(1) == True)
    a.remove(1)
    assert (a.has(1) == False)
    a.add(1)
    assert (a.has(1) == True)


if __name__ == '__main__':
    testSet()
