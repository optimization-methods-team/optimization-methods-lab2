import copy


def lup_decomposition(A):
    new_A = copy.deepcopy(A)
    n = len(new_A)
    p = [0 for _ in range(n)]
    for i in range(n):
        p[i] = i

    for k in range(n):
        pp = 0
        kk = 0
        for i in range(k, n):
            if abs(new_A[i][k]) > pp:
                pp = abs(new_A[i][k])
                kk = i

        if pp == 0:
            # print("det(matr) == 0")
            return [], []

        tmp = p[k]
        p[k] = p[kk]
        p[kk] = tmp

        for i in range(n):
            t = new_A[k][i]
            new_A[k][i] = new_A[kk][i]
            new_A[kk][i] = t

        for i in range(k + 1, n):
            new_A[i][k] = new_A[i][k] / new_A[k][k]
            for j in range(k + 1, n):
                new_A[i][j] = new_A[i][j] - new_A[i][k] * new_A[k][j]

    return p, new_A


def lu_from_matrix(A):
    n = len(A)
    L = [[0 for _ in range(len(A[0]))] for _ in range(n)]
    U = [[0 for _ in range(len(A[0]))] for _ in range(n)]
    for i in range(n):
        L[i][i] = 1

    for k in range(n):
        U[k][k] = A[k][k]
        for i in range(k + 1, n):
            L[i][k] = A[i][k]
            U[k][i] = A[k][i]

    return L, U


def dot_vector(L, y, i):
    sum_ = 0
    for j in range(len(L)):
        sum_ += L[i][j] * y[j]
    return sum_


def Gauss(A, b):
    p, new_A = lup_decomposition(A)
    if not p:
        return []
    L, U = lu_from_matrix(new_A)
    return lup_solve(L, U, p, b)


def lup_solve(L, U, p, b):
    n = len(L)
    y = [0 for _ in range(n)]
    x = [0 for _ in range(n)]

    for i in range(n):
        y[i] = b[p[i]] - dot_vector(L, y, i)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - dot_vector(U, x, i)) / U[i][i]
    return x
