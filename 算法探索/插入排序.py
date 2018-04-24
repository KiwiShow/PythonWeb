def insert_sort(lst):
    n = len(lst)
    if n == 1:
        return lst
    for i in range(1, n):
        for j in range(i, 0, -1):
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
    return lst


if __name__ == "__main__":
    testlist = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print('final:', insert_sort(testlist))
    import os.path

    print('{}'.format(os.path.dirname(__file__)))
