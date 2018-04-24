import math


def radix_sort(a, radix=10):
    """a为整数列表， radix为基数"""
    K = int(math.ceil(math.log(max(a), radix)))  # 用K位数可表示任意整数
    bucket = [[] for i in range(radix)]  # 不能用 [[]]*radix
    for i in range(1, K + 1):  # K次循环
        for val in a:
            bucket[val % (radix ** i) / (radix ** (i - 1))].append(val)  # 析取整数第K位数字 （从低到高）
        del a[:]
        for each in bucket:
            a.extend(each)  # 桶合并
        bucket = [[] for i in range(radix)]


if __name__ == "__main__":
    testlist = [17, 23, 20, 14, 12, 25, 1, 20, 81, 14, 11, 12]
    print('After selection sort:  {}'.format(radix_sort(testlist)))
