def bubble(List):
    for j in range(len(List) - 1, 0, -1):
        flag = True
        for i in range(0, j):
            if List[i] > List[i + 1]:
                flag = False
                List[i], List[i + 1] = List[i + 1], List[i]
        if flag == True:
            return List
    return List


if __name__ == "__main__":
    testlist = [27, 33, 28, 4, 2, 26, 13, 35, 8, 14]
    print('final:', bubble(testlist))

# 助记码
# i∈[0,N-1)               //循环N-1遍
#	j∈[0,N-1-i)           //每遍循环要处理的无序部分
#	  swap(j,j+1)          //两两排序（升序/降序）
