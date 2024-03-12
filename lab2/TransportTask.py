from LU_decomp import Gauss
from method_north_west_corner import *


class TransportTask:
    def combination(self, array, num):
        """Рекурсивная функция поиска различных комбинаций из списка array и количеством элементов num"""
        if num == 0:
            return [[]]
        list_ = []  # возвращаемый список комбинаций

        for j in range(0, len(array)):
            emptyArray = array[
                j]  # убираем элемент и составляем без него комбинации (потом его будем добавлять обратно)
            recurList = array[j + 1:]
            for x in self.combination(recurList, num - 1):
                list_.append([emptyArray] + x)
        return list_

    # public
    def __init__(self, c, a, b):
        self.C = c
        self.a = a
        self.b = b

    def NorthWestMethod(self):
        new_matr = meth_north_west_corner(self.C, self.a, self.b)
        return new_matr

    def MethodPotentional(self):
        new_matr = self.NorthWestMethod()
        solution_ = method_potentional(new_matr)
        return solution_

    def extreme_point_method(self):
        # Firstly transform transport task to linear program task
        # Free column
        f = copy.deepcopy(self.a)
        f.extend(self.b)
        # Matrix and vector function to minimize
        A = [[0] * (len(self.C[0]) * len(self.C)) for _ in range(len(f))]
        z = []
        for i in range(len(self.C)):
            for j in range(len(self.C[0])):
                z.append(self.C[i][j])
                A[i][j + i * len(self.C[0])] = 1
                A[len(self.C) + j][j + i * len(self.C[0])] = 1

        A.pop()  # Remove the last row from A
        f.pop()  # Remove the last element from f

        # Method itself
        set_of_indices = list(range(len(A[0])))
        solution = []
        vector_solution_and_func_c = []
        min_of_function = float('inf')
        # vector_of_indices = list(itertools.combinations(set_of_indices, len(A)))
        vector_of_indices = self.combination(set_of_indices, len(A))

        for indices in vector_of_indices:  # Checks every possible combination of columns
            # Get matrix for linear system
            sub_matr = [[A[i][j] for j in indices] for i in range(len(A))]

            # Solve linear system

            system_solution = Gauss(sub_matr, f)
            if not system_solution:
                continue

            # Check that solution is >= 0
            flag = all(val >= 0 and not (val != val) for val in system_solution)
            if not flag:
                continue

            # Add zeros to solution
            new_solution = [0] * len(z)
            for i in range(len(indices)):
                new_solution[indices[i]] = system_solution[i]

            # Check if that vector is maybe a better solution
            function_val = sum(new_solution[i] * z[i] for i in range(len(new_solution)))

            dict_sol = {"solution": new_solution, "func_val": function_val}
            vector_solution_and_func_c.append(dict_sol)

            if function_val < min_of_function:
                min_of_function = function_val
                solution = new_solution

        if not solution:
            raise Exception("No solutions found in extreme point")

        solution_min_vector = [sol["solution"] for sol in vector_solution_and_func_c
                               if sol["func_val"] == min_of_function]
        print("Count of solution:", len(solution_min_vector))
        print("Total sum:", min_of_function)

        sol = [solution[k] for k in range(len(solution))]
        x_solution = []
        i = 0
        while i < len(solution):
            list_ = sol[i: len(self.C[0])+i]
            i += len(C[0])
            x_solution.append(list_)

        return x_solution, solution_min_vector
