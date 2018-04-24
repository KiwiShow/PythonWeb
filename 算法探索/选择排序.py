def selection_sort(L):
    N = len(L)
    exchanges_count = 0
    for i in range(N - 1):
        min_index = i
        for j in range(i + 1, N):
            if L[min_index] > L[j]:
                min_index = j
        if min_index != i:
            L[min_index], L[i] = L[i], L[min_index]
            exchanges_count += 1
        print('iteration #{}: {}'.format(i, L))
    print('Total {} swappings'.format(exchanges_count))
    return L


if __name__ == "__main__":
    testlist = [17, 23, 20, 14, 12, 25, 1, 20, 81, 14, 11, 12]
    print('Before selection sort: {}'.format(testlist))
    print('After selection sort:  {}'.format(selection_sort(testlist)))


def selection_sort(l):
    N = len(l)
    for i in range(N - 1):
        min_index = i
        for j in range(i + 1, N):
            if l[min_index] > l[j]:
                min_index = j
        if min_index != i:
            l[min_index], l[i] = l[i], l[min_index]
    return l


if __name__ == "__main__":
    testlist = [17, 23, 20, 14, 12, 25, 1, 20, 81, 14, 11, 12]
    print('After selection sort:  {}'.format(selection_sort(testlist)))
