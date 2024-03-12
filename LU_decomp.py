

def lup_decomposition(A):
    n = len(A)
    p = [0 for _ in range(n)]
    for i in range(n):
        p[i] = i

    for k in range(n):
        pp = 0
        kk = 0
        for i in range(k, n):
            if abs(A[i][k]) > pp:
                pp = abs(A[i][k])
                kk = i

        if pp == 0:
            print("Error")
            return []

        p[k], p[kk] = p[kk], p[k]

        for i in range(n):
            A[k][i], A[kk][i] = A[kk][i], A[k][i]

        for i in range(k + 1, n):
            A[i][k] = A[i][k] / A[k][k]
            for j in range(k + 1, n):
                A[i][j] = A[i][j] - A[i][k] * A[k][j]

    return p


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


def lup_solve(L, U, p, b):
    n = len(L)
    y = [0 for _ in range(n)]
    x = [0 for _ in range(n)]

    for i in range(n):
        y[i] = b[p[i]] - dot_vector(L, y, i)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - dot_vector(U, x, i)) / U[i][i]
    return x


def Gauss(A, b):
    p = lup_decomposition(A)
    L, U = lu_from_matrix(A)
    return lup_solve(L, U, p, b)


