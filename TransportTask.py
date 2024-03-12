import itertools
from LU_decomp import Gauss


class TransportTask:

    def getCombinations(self, n : int, k : int, i : int, nc : int, temp: list, ret: list):
        if i == n:
            if nc == k:
                ret.append(temp)
                return ret, temp
        if nc < k:
            temp[nc] = i
            ret, temp = self.getCombinations(n, k, i + 1, nc + 1, temp, ret)
            ret, temp = self.getCombinations(n, k, i + 1, nc, temp, ret)
        return ret, temp

    def combine(self, n: int, k: int):
        temp = []
        for i in range(k):
            temp.append(0)
        ret = []
        ret, temp = self.getCombinations(n, k, 0, 0, temp, ret)
        return ret

    def draw_cycle(self, cycle, plan):
        table = [[(0.0, "") for _ in range(len(plan[0]))] for _ in range(len(plan))]

        plus_sign = "[+]"
        minus_sign = "[-]"
        empty = " - "

        # Fill table
        table[cycle[0][0]][cycle[0][1]] = (-1, plus_sign)
        for i in range(1, len(cycle)):
            table[cycle[i][0]][cycle[i][1]] = (plan[cycle[i][0]][cycle[i][1]], plus_sign if i % 2 == 0 else minus_sign)

        # Print table
        for i in range(len(table)):
            for j in range(len(table[0])):
                if table[i][j][1] == "":
                    print(empty, end=" ")
                elif table[i][j][0] >= 0:
                    print(f"{table[i][j][0]}{table[i][j][1]}", end=" ")
                else:
                    print(table[i][j][1], end=" ")
            print()

        # Print cycle
        print("cycle:")
        for i in range(len(cycle) - 1):
            print(f"({cycle[i][0]}, {cycle[i][1]}) -> ", end="")
        print(f"({cycle[-1][0]}, {cycle[-1][1]})\n")

    def draw_plan(self, basis, plan):
        print("plan:")
        table = [[(0.0, False) for _ in range(len(plan[0]))] for _ in range(len(plan))]
        empty = " - "

        # Fill table
        for i in range(len(basis)):
            table[basis[i][0]][basis[i][1]] = (plan[basis[i][0]][basis[i][1]], True)

        # Print table
        for i in range(len(table)):
            for j in range(len(table[0])):
                if not table[i][j][1]:
                    print(empty, end=" ")
                else:
                    print(table[i][j][0], end=" ")
            print()
        print()

    #public
    def __init__(self, c, a, b):
        self.C = c
        self.a = a
        self.b = b
        self.NorthWestMethod()

    def NorthWestMethod(self):
        X = [[0] * len(self.b) for _ in range(len(self.a))]
        nw_cell_x = 0
        nw_cell_y = 0
        basis = []

        while nw_cell_y < len(self.a) and nw_cell_x < len(self.b):
            basis.append((nw_cell_y, nw_cell_x))
            col_amount = self.b[nw_cell_x]
            row_amount = self.a[nw_cell_y]

            for i in range(nw_cell_x):
                row_amount -= X[nw_cell_y][i]

            for i in range(nw_cell_y):
                col_amount -= X[i][nw_cell_x]

            if col_amount < row_amount:
                X[nw_cell_y][nw_cell_x] = col_amount
                nw_cell_x += 1
            else:
                X[nw_cell_y][nw_cell_x] = row_amount
                nw_cell_y += 1

        if nw_cell_y < len(self.a) - 1 or nw_cell_x < len(self.b) - 1:
            print("Vovas made a huge mistake")

        return X, basis

    def BuildPotentials(self, basis):
        U = [0]*len(self.a)
        V = [0]*len(self.b)
        filled_U = [basis[0][1]]
        filled_V = []
        U[basis[0][1]] = 0
        is_done = False

        while not is_done:
            is_done = True
            is_changed = False
            remember_x = -1

            for i in range(len(basis)):
                cell_y, cell_x = basis[i]

                is_x = cell_x in filled_U
                is_y = cell_y in filled_V

                if is_x and not is_y:
                    U[cell_y] = self.C[cell_y][cell_x] - V[cell_x]
                    filled_U.append(cell_y)
                    is_changed = True
                elif not is_x and is_y:
                    V[cell_x] = self.C[cell_y][cell_x] - U[cell_y]
                    filled_V.append(cell_x)
                    is_changed = True
                elif not is_x and not is_y:
                    remember_x = cell_x

                if not (is_x and is_y):
                    is_done = False

            if not is_changed and not is_done:
                V[remember_x] = 0
                filled_V.append(remember_x)

        return U, V

    def FindCycle(self, vertices_for_x, vertices_for_y, start, cur_path, go_vertical=False):
        if not cur_path:
            cur_path.append(start)

        for i in range(len(cur_path) - 1):
            if cur_path[i] == cur_path[-1]:
                return 0

        if len(cur_path) > 2 and (cur_path[-1][0] == start[0] or cur_path[-1][1] == start[1]):
            return len(cur_path)

        y_to_check, x_to_check = cur_path[-1]

        best = float('inf')
        best_res = []

        if not go_vertical:
            for i in vertices_for_y[y_to_check]:
                cur_path.append((y_to_check, i))
                res = self.FindCycle(vertices_for_x, vertices_for_y, start, cur_path, True)

                if res != 0 and len(cur_path) < best:
                    best_res = cur_path[:]
                    best = res

                cur_path.pop()

        else:
            for i in vertices_for_x[x_to_check]:
                cur_path.append((i, x_to_check))
                res = self.FindCycle(vertices_for_x, vertices_for_y, start, cur_path, False)

                if res != 0 and len(cur_path) < best:
                    best_res = cur_path[:]
                    best = res

                cur_path.pop()

        if best != float('inf'):
            cur_path[:] = best_res

        return len(best_res)

    def PotentialMethod(self):
        Xb = self.NorthWestMethod()
        X = Xb[0]
        basis = Xb[1]
        basis_y_for_x = [[] for _ in range(len(self.b))]
        basis_x_for_y = [[] for _ in range(len(self.a))]

        for k in range(len(basis)):
            i, j = basis[k]
            basis_x_for_y[i].append(j)
            basis_y_for_x[j].append(i)

        while True:
            uv = self.BuildPotentials(basis)
            U, V = uv

            cur_min_x = 0
            cur_min_y = 0
            value = self.C[0][0] - U[0] - V[0]

            for i in range(len(self.C)):
                for j in range(len(self.C[0])):
                    if self.C[i][j] - U[i] - V[j] < value:
                        cur_min_x = j
                        cur_min_y = i
                        value = self.C[i][j] - U[i] - V[j]

            if value >= 0:
                break

            cycle = []
            res = self.FindCycle(basis_y_for_x, basis_x_for_y, (cur_min_y, cur_min_x), cycle)

            self.draw_plan(basis, X)
            self.draw_cycle(cycle, X)

            if res < 3:
                raise ValueError("Cannot find cycle")

            min_cell = cycle[1]

            for i in range(1, len(cycle), 2):
                if X[cycle[i][0]][cycle[i][1]] < X[min_cell[0]][min_cell[1]]:
                    min_cell = cycle[i]

            val = X[min_cell[0]][min_cell[1]]

            for i in range(len(cycle)):
                X[cycle[i][0]][cycle[i][1]] += (((i + 1) % 2) * 2 - 1) * val

            for i in range(len(basis)):
                if basis[i] == min_cell:
                    basis.pop(i)
                    break

            for i in range(len(basis_x_for_y[min_cell[0]])):
                if basis_x_for_y[min_cell[0]][i] == min_cell[1]:
                    basis_x_for_y[min_cell[0]].pop(i)
                    break

            for i in range(len(basis_y_for_x[min_cell[1]])):
                if basis_y_for_x[min_cell[1]][i] == min_cell[0]:
                    basis_y_for_x[min_cell[1]].pop(i)
                    break

            basis.append((cur_min_y, cur_min_x))
            basis_x_for_y[cur_min_y].append(cur_min_x)
            basis_y_for_x[cur_min_x].append(cur_min_y)

        total_sum = sum(X * self.C)
        print(f"Total sum: {total_sum}")

        return X


    def extreme_point_method(self):
        # Firstly transform transport task to linear program task
        # Free column
        f = self.a
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
        min_of_function = float('inf')
        vector_of_indices = list(itertools.combinations(set_of_indices, len(A)))

        for indices in vector_of_indices:  # Checks every possible combination of columns
            # Get matrix for linear system
            sub_matr = [[A[i][j] for j in indices] for i in range(len(A))]

            # Solve linear system
            try:
                system_solution = Gauss(sub_matr, f)
            except Exception as ex:
                raise ex

            # Check that solution is >= 0
            flag = all(val >= 0 and not (val != val) for val in system_solution)
            if not flag:
                continue

            # Add zeros to solution
            new_solution = [0] * len(f)
            for i in range(len(indices)):
                new_solution[indices[i]] = system_solution[i]

            # Check if that vector is maybe a better solution
            function_val = sum(new_solution[i] * z[i] for i in range(len(new_solution)))
            if function_val < min_of_function:
                min_of_function = function_val
                solution = new_solution

        if not solution:
            raise Exception("No solutions found in extreme point")

        print("Total sum:", sum(solution[i] * z[i] for i in range(len(solution))))

        sol = [[solution[k] for k in range(len(solution))]]
        k = 1
        for i in range(len(self.C)):
            row = [solution[k] for k in range(k, k + len(self.C[0]))]
            sol.append(row)
            k += len(self.C[0])

        return sol
