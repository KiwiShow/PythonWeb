class Node():
    def __init__(self, element=None, next=None):
        self.element = element
        self.next = next

    def __repr__(self):
        return str(self.element)


class Stack():
    def __init__(self):
        self.head = Node()

    def is_empty(self):
        return self.head.next is None

    def push(self, element):
        self.head.next = Node(element, self.head.next)

    def pop(self):
        node = self.head.next
        if not self.is_empty():
            self.head.next = node.next
        return node

    def top(self):
        return self.head.next


##############################################
# push---> head-4-3-2-1
#         pop---^---top
##############################################


# 测试函数
def test():
    s = Stack()

    s.push(1)
    s.push(2)
    s.push(3)
    s.push(4)

    print(s.pop())
    print(s.pop())
    print(s.pop())
    print(s.pop())
    # 返回None，因为没数了
    print(s.pop())


if __name__ == '__main__':
    # 运行测试函数
    test()


# 4
# 3
# 2
# 1
# None
