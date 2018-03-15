class Tree(object):
    def __init__(self, element=None):
        self.element = element
        self.left = None
        self.right = None

    def traversal(self):
        print(self.element)
        if self.left is not None:
            self.left.traversal()
        if self.right is not None:
            self.right.traversal()


def test():
     t = Tree(0)
     left = Tree(1)
     right = Tree(2)
     t.left = left
     t.right = right
     # 遍历
     t.traversal()


if __name__ == '__main__':
    test()
