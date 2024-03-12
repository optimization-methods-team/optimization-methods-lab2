from potentional_method import *


def min_(a: int, b: int):
    if a < b:
        return a
    return b


def print_matrix(Cc: list, a: list, b: list):
    n = len(a)
    m = len(b)
    for j in range(m+1):
        print(" _________________ ", end="")
    print(" _________________ ")

    print("|                 |", end="")
    for j in range(m):
        print("|       B_{j}       |".format(j=j+1), end="")
    print("|                 |")

    for j in range(m+1):
        print("|-----------------|", end="")
    print("|-----------------|")

    for i in range(n):
        print("|                 |", end="")
        for j in range(m):
            print("|  {c:5d} :        |".format(c=Cc[i][j]["c"]), end="")
        print("|                 |")

        print("|       A_{i}       |".format(i=i+1), end="")
        for j in range(m):
            print("|--------:        |", end="")
        print("|      {a:5d}      |".format(a=a[i]))

        print("|                 |", end="")
        for j in range(m):
            volume = Cc[i][j]["volume"]
            if volume == -2:
                print("|                 |", end="")
                continue
            if volume == -1:
                print("|            x    |", end="")
                continue
            print("|          \033[33m{v:5d}\033[0m  |".format(v=volume), end="")
        print("|                 |")

        for j in range(m + 1):
            print("|-----------------|", end="")
        print("|-----------------|")

    print("|                 |", end="")
    for j in range(m):
        print("|      {b:5d}      |".format(b=b[j]), end="")
    print("|                 |")

    for j in range(m + 1):
        print(" _________________ ", end="")
    print(" _________________ ")
    print()
    print()


def meth_north_west_corner(Cc: list, aa: list, bb: list):
    """
    Метод северо-западного угла
    :param Cc: матрица перевозок
    :param aa: объёмы поставщиков
    :param bb: объёмы заказчиков
    :return: матрица с закрытыми и открытыми клетками
    """
    print("--МЕТОД СЕВЕРО-ЗАПАДНОГО УГЛА--")
    new_C = []  # новая матрица клетки которых являются словарём
    a = copy.deepcopy(aa)
    b = copy.deepcopy(bb)

    for i in range(len(a)):
        new_row = []
        for j in range(len(b)):
            dict_el = {"c": Cc[i][j], "volume": -2}  # пока открытость (есть объём) и закрытость
            # (закрытость обозначим через -1) неизвестны
            new_row.append(dict_el)

        new_C.append(new_row)

    n = len(aa)  # количество поставщиков
    m = len(bb)  # количество заказчиков

    # координаты текущей северо - западной клетки
    i = 0  # начинаем с левого верхнего угла
    j = 0
    iter = 0
    while i != n and j != m:  # такое будет возможно только, когда дойдём до правого нижнего угла и выйдем из него
        print("Итерация №{it}".format(it=iter))
        print_matrix(new_C, a, b)
        iter += 1

        volume_cur_corner = min(a[i], b[j])  # объём для текущей с-з клетки
        new_C[i][j]["volume"] = volume_cur_corner  # запоминаем объём текущей с-з клетки

        new_volume_a_i = a[i] - volume_cur_corner  # считаем новый объём для поставщика (что у него останется)
        a[i] = new_volume_a_i  # обновляем объём поставщика

        new_volume_b_j = b[j] - volume_cur_corner  # считаем новый объём для заказчика
        # (столько осталось ему допоставить)
        b[j] = new_volume_b_j  # обновляем объём заказчика

        # у поставщика не осталось товара и удовлетворили объёму заказчика
        if new_volume_a_i == 0 and new_volume_b_j == 0:
            # нужно одну из соседних клеток справа или снизу закрыть, а другую сделать = 0
            # так как изначально закрыли все клетки, то нужно только какой-то придать объём 0, и сдвиг и номера строки
            # и номера столбца на 1

            # проверяем, что эта ситуация не у правого нижнего угла
            if i != n - 1 and j != m - 1:
                new_C[i][j + 1]["volume"] = 0  # для удобства будем всегда клетку слева занулять

                # закрываем столбец с индексом j:
                for i_id in range(i + 1, n):
                    new_C[i_id][j]["volume"] = -1

                # закрываем строку с индексом i:
                for j_id in range(j + 2, m):
                    new_C[i][j_id]["volume"] = -1

            j += 1
            i += 1
            continue

        if new_volume_a_i == 0:
            # закрываем строку с индексом i:
            for j_id in range(j + 1, m):
                new_C[i][j_id]["volume"] = -1
            # сдвигаемся по клетке вниз
            i += 1
            continue

        if new_volume_b_j == 0:
            # закрываем столбец с индексом j:
            for i_id in range(i + 1, n):
                new_C[i_id][j]["volume"] = -1
            # сдвигаемся по клетке вправо
            j += 1
            continue

    print("Матрица после метода северо-западного угла")
    print_matrix(new_C, a, b)
    return new_C


C = [[8, 6, 5, 5, 8], [21, 8, 6, 7, 9], [7, 6, 18, 4, 9], [10, 11, 6, 12, 9]]
a = [21, 31, 16, 21]
b = [13, 16, 16, 33, 11]

#new_matr = meth_north_west_corner(C, a, b)
#solution = method_potentional(new_matr)
#print(solution)
