import matplotlib.pyplot as plt
import math

def pre_processing(filename):
    file = open(filename)
    lines = file.readlines()
    cities = [[]]
    n = int(lines[0])
    for l in lines[1:]:
        cities.append(list(map(float, l.split())))
    adj_mat = [[None] * (n+1)  for i in range(n+1)]


    x = [float(i[0]) for i in cities[1:]]
    y = [float(i[1]) for i in cities[1:]]
    plt.scatter(x, y)
    plt.show()

    for i in range(1, n+1):
        for j in range(1, n+1):
            if adj_mat[j][i]:
                adj_mat[j][i] = adj_mat[i][j]
            else:
                c1 = cities[i]
                c2 = cities[j]  
                adj_mat[j][i] = math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)
    return adj_mat, n

def get_bin(n, bits):
    if n == 0:
        return [0]
    res = list()
    digit = n-1
    cur = 1 << digit
    while cur < 1 << bits:
        for i in get_bin(n-1, digit):
            res.append(cur|i)
        digit += 1
        cur = 1 << digit
    return res

def get_sets(n):
    sets = dict()
    for i in range(0, n + 1):
        #print(i)
        sets[i] = get_bin(i, n)
    return sets

#sets: dict
#keys: subproblem size
#value: binary set
def get_ele(set_hash):
    set_hash >>= 1
    k = 2
    res = set()
    while set_hash:
        if set_hash & 1:
            res.add(k)
        k += 1
        set_hash >>= 1
    return res

def TSP(n,adj_mat):

    sets = get_sets(n)
    A = {}
    #deal with base case
    for i in range(1<<n):
        A[i,1] = float("inf")
    A[1,1] = 0

    for m in range(2, n+1):
        print('m=', m)
        for subset in sets[m]:
            if subset & 1:
                elements = get_ele(subset)
                for j in elements:
                    min_ = float("inf")
                    for k in range(1, n+1):
                        if k!= j:
                            if (subset ^ 1<<j-1,k) in A:
                                min_ = min(min_, A[subset ^ 1<<j-1, k] + adj_mat[k][j])
                            A[subset,j] = min_
    return A
if __name__ == '__main__':
    n, adj_mat = pre_processing('tsp.txt')
    A = TSP(n,adj_mat)
    res = float("inf")
    for j in range(2, n+1):
        res = min(res, A[(1<<n)-1, j] + adj_mat[j][1])
    print(res)