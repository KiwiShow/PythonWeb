def quicksort(a):
    if len(a) <= 1:
        return a  # 如果a為一位數則直接傳回a
    l = [x for x in a[1:] if x <= a[0]]  # 輸出排序後的比a[0]小的數列
    r = [x for x in a[1:] if x > a[0]]  # 輸出排序後的比a[0]大的數列
    return quicksort(l) + [a[0]] + quicksort(r)


if __name__ == "__main__":
    testlist = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print('final:', quicksort(testlist))
