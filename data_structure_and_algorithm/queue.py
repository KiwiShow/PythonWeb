class Node():
    def __init__(self, element=None, next=None):
        self.element = element
        self.next = next

    def __repr__(self):
        return str(self.element)


class Queue():
    def __init__(self):
        self.head = Node()
        self.tail = self.head

    def is_empty(self):
        return self.head.next is None

    def enqueue(self, element):
        n = Node(element)
        self.tail.next = n
        self.tail = n

    def dequeue(self):
        node = self.head.next
        if not self.is_empty():
            self.head.next = node.next
        return node

##############################################
#           head-1-2-3-4(tail) <---enqueue
#      dequeue---^
##############################################


# 测试函数
def test():
    q = Queue()

    q.enqueue(1)
    q.enqueue(2)
    q.enqueue(3)
    q.enqueue(4)

    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    print(q.dequeue())
    # 返回None，因为没数了
    print(q.dequeue())


if __name__ == '__main__':
    # 运行测试函数
    test()


# 1
# 2
# 3
# 4
# None
