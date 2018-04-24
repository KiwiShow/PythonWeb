from collections import deque


def merge_sort(lst):
    if len(lst) <= 1:
        return lst

    def merge(left, right):
        merged, left, right = deque(), deque(left), deque(right)
        while left and right:
            merged.append(left.popleft() if left[0] <= right[0] else right.popleft())  # deque popleft is also O(1)
        merged.extend(right if right else left)
        return list(merged)

    middle = int(len(lst) // 2)
    left = merge_sort(lst[:middle])
    right = merge_sort(lst[middle:])
    return merge(left, right)


if __name__ == "__main__":
    testlist = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print('final:', merge_sort(testlist))


# type 2

def merge(left, right):
    i, j = 0, 0
    result = []
    # 到最后任何一个数组先出栈完，就将另外i一个数组里的所有元素追加到新数组后面。
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result += left[i:]
    result += right[j:]
    return result


def merge_sort(lists):
    # 归并排序
    if len(lists) <= 1:
        return lists
    num = int(len(lists) / 2)
    left = merge_sort(lists[:num])
    right = merge_sort(lists[num:])
    return merge(left, right)


if __name__ == "__main__":
    testlist = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print('final:', merge_sort(testlist))
