class Node(object):
    def __init__(self, element=-1):
        self.element = element
        self.next = None


class LinkedList(object):
    def __init__(self):
        self.head = None

    def is_empty(self):
        return self.head is None

    def length(self):
        index = 0
        node = self.head
        while node is not None:
            index += 1
            node = node.next
        return index

    def find(self, element):
        node = self.head
        while node is not None:
            if node.element == element:
                break
            node = node.next
        return node

    def _node_at_index(self, index):
        i = 0
        node = self.head
        while node is not None:
            if i == index:
                return node
            node = node.next
            i += 1
        return None

    def element_at_index(self, index):
        node = self._node_at_index(index)
        return node.element

    def insert_before_index(self, position, element):
        newNode = Node(element)
        before_inserNode = self._node_at_index(position - 1)
        insertNode = self._node_at_index(position)
        before_inserNode.next = newNode
        newNode.next = insertNode

    def insert_after_index(self, position, element):
        newNode = Node(element)
        insertNode = self._node_at_index(position)
        after_insertNode = self._node_at_index(position + 1)
        insertNode.next = newNode
        newNode.next = after_insertNode

    def first_object(self):
        if self.is_empty() is True:
            return None
        else:
            return self.head

    def last_object(self):
        node = self.head
        lastNode = None
        while node is not None:
            lastNode = node
            node = node.next
        return lastNode

    def append(self, node):
        if self.head is None:
            self.head.next = node
        else:
            last_node = self.last_object()
            last_node.next = node
            node.front = last_node

    def display(self):
        r = []
        node = self.head
        while node is not None:
            r.append(node.element)
            node = node.next
        return r


def test():
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    a.next = b
    b.next = c
    c.next = d
    l = LinkedList()
    l.head = a
    print(l.display())
    print('the length is ', l.length())
    print('empty or not ? ', l.is_empty())
    print('find 3 =====> ', l.find(3).element)
    print('index 2 is  ', l.element_at_index(2))
    print('first object is  ', l.first_object().element)
    print('last object is  ', l.last_object().element)
    l.append(Node(5))
    print('append object 5 is  ', l.display())
    l.insert_after_index(2, 888)
    print('insert_after_index 2 is  ', l.display())
    l.insert_before_index(5, 999)
    print('insert_before_index 5 is  ', l.display())


if __name__ == '__main__':
    test()
