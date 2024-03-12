import copy
import random
import scipy as sc
from LU_decomp import *


def print_matrix_with_curve(matrix: list, start_corner_in_curve: list, u_list: list, v_list: list):
    """Печать матрицы и кривой пересчёта"""
    n = len(matrix)
    m = len(matrix[0])

    for j in range(m+1):
        print(" _________________ ", end="")
    print(" _________________ ")

    print("|                 |", end="")
    for j in range(m):
        print("|       B_{j}       |".format(j=j + 1), end="")
    print("|        U        |")

    for j in range(m+1):
        print("|-----------------|", end="")
    print("|-----------------|")

    for i in range(n):
        print("|                 |", end="")
        for j in range(m):
            print("|{c:5d}   :    \033[1m\033[35m{sign:1s}\033[0m   |".format(c=matrix[i][j]["c"],
                                                                              sign=matrix[i][j]["sign"]),
                  end="")
        print("|                 |")

        print("|       A_{i}       |".format(i=i + 1), end="")
        for j in range(m):
            print("|--------:        |", end="")
        print("|       {u:3d}       |".format(u=u_list[i]))

        print("|                 |", end="")
        for j in range(m):
            volume = matrix[i][j]["volume"]
            if volume == -2:
                print("|                 |", end="")
            if volume == -1:
                if i == start_corner_in_curve[0] and j == start_corner_in_curve[1]:
                    print("|         \033[1m\033[31m{v:5s}\033[0m   |".format(v="x"), end="")
                else:
                    print("|            x    |", end="")
            else:
                print("|     \033[1m\033[33m{v:5d}\033[0m       |".format(v=volume), end="")
        print("|                 |")

        for j in range(m+1):
            print("|                 |", end="")
        print("|                 |")

        print("|                 |", end="")
        for j in range(m):
            direct_list = matrix[i][j]["direct"]
            if not direct_list:
                direct = ""
            else:
                direct = direct_list[0]
            print("|         \033[32m{d:3s}\033[0m     |".format(d=direct), end="")
        print("|                 |")

        print("|                 |", end="")
        for j in range(m):
            direct_list = matrix[i][j]["direct"]
            if not direct_list or len(direct_list) == 1:
                direct = ""
            else:
                direct = direct_list[1]
            print("|         \033[32m{d:3s}\033[0m     |".format(d=direct), end="")
        print("|                 |")

        for j in range(m+1):
            print("|-----------------|", end="")
        print("|-----------------|")

    print("|        V        |", end="")
    for j in range(m):
        print("|      {v:5d}      |".format(v=v_list[j]), end="")
    print("|                 |")

    for j in range(m + 1):
        print(" _________________ ", end="")
    print(" _________________ ")
    print()
    print()
    print()


def print_final_matrix(matrix: list):
    """Печать финальной матрицы"""
    n = len(matrix)
    m = len(matrix[0])

    for j in range(m):
        print(" _________________ ", end="")
    print(" _________________ ")

    print("|                 |", end="")
    for j in range(m-1):
        print("|       B_{j}       |".format(j=j + 1), end="")
    print("|       B_{j}       |".format(j=m))

    for i in range(n):
        for j in range(m):
            print("|-----------------|", end="")
        print("|-----------------|")

        print("|                 |", end="")
        for j in range(m-1):
            print("|{c:5d}   :    \033[1m\033[35m{sign:1s}\033[0m   |".format(c=matrix[i][j]["c"],
                                                                              sign=matrix[i][j]["sign"]),
                  end="")
        print("|{c:5d}   :    \033[1m\033[35m{sign:1s}\033[0m   |".format(c=matrix[i][m-1]["c"],
                                                                          sign=matrix[i][m-1]["sign"]))

        print("|       A_{i}       |".format(i=i + 1), end="")
        for j in range(m-1):
            print("|--------:        |", end="")
        print("|--------:        |")

        print("|                 |", end="")
        for j in range(m-1):
            volume = matrix[i][j]["volume"]
            if volume == -2:
                print("|                 |", end="")
            if volume == -1:
                print("|            x    |", end="")
            else:
                print("|     \033[1m\033[33m{v:5d}\033[0m       |".format(v=volume), end="")

        volume = matrix[i][m-1]["volume"]
        if volume == -2:
            print("|                 |")
        if volume == -1:
            print("|            x    |")
        else:
            print("|     \033[1m\033[33m{v:5d}\033[0m       |".format(v=volume))

    for j in range(m):
        print(" _________________ ", end="")
    print(" _________________ ")
    print()
    print()
    print()


def cell_count_analysis(Cc: list):
    """
    Анализ числа заполненных клеток и решение СЛАУ по заполненным клеткам
    :return:
    """

    new_V_matr = []
    new_U_matr = []
    vector_price = []
    count_non_empty_cells = 0
    list_empty_cells = []

    n = len(Cc)
    m = len(Cc[0])

    v_list = [0 for _ in range(m)]  # список потенциалов для заказчиков
    u_list = [0 for _ in range(n)]  # список потенциалов для поставщиков (причём учитываем, что будем принимать u[0]=0

    for i in range(n):
        for j in range(m):
            if Cc[i][j]["volume"] == -1:
                list_empty_cells.append([i, j])  # запоминаем пустую клетку
                continue

            count_non_empty_cells += 1
            cur_u_list = [0 for _ in range(n - 1)]  # без u[0]
            cur_v_list = [0 for _ in range(m)]

            # составление уравнения (одна строка таблицы) по формуле: v[j]-u[i]
            cur_v_list[j] = 1

            if i != 0:
                cur_u_list[i - 1] = -1

            new_V_matr.append(cur_v_list)
            new_U_matr.append(cur_u_list)

            vector_price.append(Cc[i][j]["c"])

    if count_non_empty_cells != n + m - 1:
        print("Error")
        return [], [], []

    matrix = []

    for i in range(count_non_empty_cells):
        new_row = [k for k in new_V_matr[i] + new_U_matr[i]]
        matrix.append(new_row)

    solution = Gauss(matrix, vector_price)

    for id_ in range(m):
        v_list[id_] = int(solution[id_])

    i = 1
    for id_ in range(m, len(solution)):
        u_list[i] = int(solution[id_])
        i += 1

    return v_list, u_list, list_empty_cells


def validation_opt_(Cc: list, v_list: list, u_list: list, list_empty_cells: list):
    """Проверка задачи на оптимальность"""

    for id_ in list_empty_cells:
        i = id_[0]
        j = id_[1]

        alpha = v_list[j] - u_list[i]
        c_i_j = Cc[i][j]["c"]
        if alpha - c_i_j > 0:
            return False

    return True


list_dict_corner_in_curve = []  # список клеток содержащихся в кривой


def add_dict_corner(i: int, j: int, direct: int):
    dict_corner = {"corner": [i, j],
                   "direct": direct}  # здесь будем хранить подошедший узел и напрвление, которое использовали из него
    list_dict_corner_in_curve.append(dict_corner)


def reading_curve(i: int, j: int, matrix: list, start_corner: list, direction: int):
    """
    Построение кривой пересчёта
    :param i: строка текущей клетка
    :param j: столбец текущей клетки
    :param matrix: матрица, в которой строим кривую
    :param start_corner: клетка, из которой начинали построение кривой
    :param direction: направление, в котором ведём пересчёт
    ( 0 - стартовое направление, 1 - вниз, 2 - влево, 3 - вверх, 4 - вправо
    """

    if i == start_corner[0] and j == start_corner[1] and direction != 0:
        return True

    if i < 0 or i >= len(matrix) or j < 0 or j >= len(matrix[0]):  # вышли за рамки матрицы
        return False

    # если клетка пустая(закрытая), то сменить напрвление нельзя
    if matrix[i][j]["volume"] == -1:
        match direction:
            case 1:
                if reading_curve(i + 1, j, matrix, start_corner, 1):
                    add_dict_corner(i, j, 1)
                    return True
            case 2:
                if reading_curve(i, j - 1, matrix, start_corner, 2):
                    add_dict_corner(i, j, 2)
                    return True
            case 3:
                if reading_curve(i - 1, j, matrix, start_corner, 3):
                    add_dict_corner(i, j, 3)
                    return True
            case 4:
                if reading_curve(i, j + 1, matrix, start_corner, 4):
                    add_dict_corner(i, j, 4)
                    return True
            case 0:  # можем пойти в любое направление
                list_dict_corner_in_curve.clear()
                if reading_curve(i + 1, j, matrix, start_corner, 1):
                    add_dict_corner(i, j, 1)
                    return True
                if reading_curve(i, j - 1, matrix, start_corner, 2):
                    add_dict_corner(i, j, 2)
                    return True
                if reading_curve(i - 1, j, matrix, start_corner, 3):
                    add_dict_corner(i, j, 3)
                    return True
                if reading_curve(i, j + 1, matrix, start_corner, 4):
                    add_dict_corner(i, j, 4)
                    return True

    # если клетка заполенна, то можем выбрать любое напрвление
    if matrix[i][j]["volume"] > -1:
        # убираем "лишние" переходы (если, пришли снизу, то вниз нет смысла идти и тд)
        match direction:
            case 1:  # пришли сверху -> нет смысла идти наверх
                if reading_curve(i + 1, j, matrix, start_corner, 1):
                    add_dict_corner(i, j, 1)
                    return True
                if reading_curve(i, j - 1, matrix, start_corner, 2):
                    add_dict_corner(i, j, 2)
                    return True
                if reading_curve(i, j + 1, matrix, start_corner, 4):
                    add_dict_corner(i, j, 4)
                    return True
                return False

            case 2:  # пришли справа -> нет смысла идти направо
                if reading_curve(i + 1, j, matrix, start_corner, 1):
                    add_dict_corner(i, j, 1)
                    return True
                if reading_curve(i, j - 1, matrix, start_corner, 2):
                    add_dict_corner(i, j, 2)
                    return True
                if reading_curve(i - 1, j, matrix, start_corner, 3):
                    add_dict_corner(i, j, 3)
                    return True
                return False

            case 3:  # пришли снизу -> нет смысла идти вниз
                if reading_curve(i, j - 1, matrix, start_corner, 2):
                    add_dict_corner(i, j, 2)
                    return True
                if reading_curve(i - 1, j, matrix, start_corner, 3):
                    add_dict_corner(i, j, 3)
                    return True
                if reading_curve(i, j + 1, matrix, start_corner, 4):
                    add_dict_corner(i, j, 4)
                    return True
                return False

            case 4:  # пришли слева -> нет смысла идти налево
                if reading_curve(i + 1, j, matrix, start_corner, 1):
                    add_dict_corner(i, j, 1)
                    return True
                if reading_curve(i - 1, j, matrix, start_corner, 3):
                    add_dict_corner(i, j, 3)
                    return True
                if reading_curve(i, j + 1, matrix, start_corner, 4):
                    add_dict_corner(i, j, 4)
                    return True
                return False  # ни одно из направлений не подошло


def list_corner_replace_direction(list_corner_in_curve: list):
    direct_ = list_corner_in_curve[0]["direct"]
    list_corner_replace = [list_corner_in_curve[0]]
    for corner in list_corner_in_curve:
        if direct_ != corner["direct"]:
            list_corner_replace.append(corner)
        direct_ = corner["direct"]
    return list_corner_replace


def placement_sign_and_direct(matrix: list, list_corner_in_curve: list):
    """
    Расставление знаков и напрвления для элементов кривой-пересчёта
    """
    list_volume_for_minus = []
    new_matrix = copy.deepcopy(matrix)
    start_corner = list_corner_in_curve[0]["corner"]
    list_corner_replace_direct = list_corner_replace_direction(list_corner_in_curve)

    for dict_corner in list_corner_in_curve:
        corner = dict_corner["corner"]
        direct = dict_corner["direct"]
        i = corner[0]
        j = corner[1]
        match direct:
            case 1:
                new_matrix[i][j]["direct"].append("\\/")
            case 2:
                new_matrix[i][j]["direct"].append("<--")
            case 3:
                new_matrix[i][j]["direct"].append("/\\")
            case 4:
                new_matrix[i][j]["direct"].append("-->")

    count_corner_change_of_direction = 0
    for dict_corner in list_corner_replace_direct:
        corner = dict_corner["corner"]
        i = corner[0]
        j = corner[1]
        if new_matrix[i][j]["volume"] > -1 or (i == start_corner[0] and j == start_corner[1]):
            count_corner_change_of_direction += 1

            if count_corner_change_of_direction % 2 != 0:
                new_matrix[i][j]["sign"] = "+"
                continue

            new_matrix[i][j]["sign"] = "-"
            list_volume_for_minus.append(new_matrix[i][j]["volume"])

    return list_volume_for_minus, new_matrix


def find_theta(list_volume: list):
    min_ = list_volume[0]
    for volume in list_volume:
        if volume < min_:
            min_ = volume

    return min_


def matrix_recalculation(Cc: list, theta: int, start_corner: list):
    """Пересчёт матрицы, после того как нашли theta"""

    count_zero_cell = 0  # количество обнуляемых переменных
    matrix = []
    for i in range(len(Cc)):
        for j in range(len(Cc[0])):
            new_volume = -1
            if Cc[i][j]["volume"] > -1:
                if Cc[i][j]["sign"] == "+":
                    new_volume = Cc[i][j]["volume"] + theta

                if Cc[i][j]["sign"] == "-":
                    new_volume = Cc[i][j]["volume"] - theta

                Cc[i][j]["sign"] = ""  # "снимаем" знак с элемента
                Cc[i][j]["direct"] = []  # "снимаем" направление
                if new_volume == 0:
                    count_zero_cell += 1
                    if count_zero_cell > 1:  # больше одной нулевой клетки закрыть нельзя
                        Cc[i][j]["volume"] = 0
                        continue

                    Cc[i][j]["volume"] = -1  # закрываем клетку
                    continue

                if new_volume > 0:
                    Cc[i][j]["volume"] = new_volume
                continue

            if i == start_corner[0] and j == start_corner[1]:
                Cc[i][j]["volume"] = theta
                Cc[i][j]["sign"] = ""  # "снимаем" знак с элемента

            Cc[i][j]["direct"] = []  # "снимаем" направление

    matrix = copy.deepcopy(Cc)
    return matrix


def solution_matrix_creation(Cc: list):
    """Создание матрицы решения транспортной задачи"""
    sol_matrix = [[0 for _ in range(len(Cc[0]))] for _ in range(len(Cc))]
    for i in range(len(Cc)):
        for j in range(len(Cc[0])):
            if Cc[i][j]["volume"] >= 0:
                sol_matrix[i][j] = Cc[i][j]["volume"]

    return sol_matrix


def method_potentional(Cc: list):
    n = len(Cc)
    m = len(Cc[0])

    transport_table = []

    for i in range(n):
        new_row = []
        for j in range(m):
            dict_el = Cc[i][j]
            dict_el["sign"] = ""  # дальше знак будет измменяться только у элементов цепочки пересчёта
            dict_el["direct"] = []  # здесь будем указывать направление ломаной пересчёта
            new_row.append(dict_el)

        transport_table.append(new_row)

    print("__МЕТОД ПОТЕНЦИАЛОВ__")
    v, u, empty_cell = cell_count_analysis(transport_table)
    iter = 1
    while not validation_opt_(transport_table, v, u, empty_cell):
        close_corner = random.choice(empty_cell)
        if not reading_curve(close_corner[0], close_corner[1], transport_table, close_corner, 0):
            return []

        list_corner_in_curve = list_dict_corner_in_curve[::-1]
        list_volume_for_minus, new_transport_table = placement_sign_and_direct(transport_table, list_corner_in_curve)

        print("Итерация №{it}".format(it=iter))
        print_matrix_with_curve(new_transport_table, list_corner_in_curve[0]["corner"], u, v)
        theta = find_theta(list_volume_for_minus)

        new_transport = matrix_recalculation(new_transport_table, theta, list_corner_in_curve[0]["corner"])

        v, u, empty_cell = cell_count_analysis(new_transport)

        if v == [] and u == [] and empty_cell == []:
            print("Error in recalculation")
            break

        transport_table = copy.deepcopy(new_transport)
        iter += 1

    print("Транспортная матрица с оптимальным решением")
    print_final_matrix(transport_table)
    solution_x = solution_matrix_creation(transport_table)
    return solution_x
