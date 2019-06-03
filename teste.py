if __name__ == '__main__':
    n = int(input())
    arr = map(int, input().split())

    maxArr = 0
    segMaxArr = 0
    for i in arr:
        if i > maxArr:
            maxArr = i

    for x in arr:
        if x > segMaxArr and x < maxArr:
            segMaxArr = x

    print(segMaxArr)