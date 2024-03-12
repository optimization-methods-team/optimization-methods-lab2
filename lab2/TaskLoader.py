from TransportTask import TransportTask


class TaskLoader:
    def __init__(self):
        self.is_phantom_store = False
        self.is_phantom_storage = False

    def load(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        N, M = map(int, lines[0].split())
        matrix_C = [list(map(int, line.split())) for line in lines[1:N+1]]
        A = list(map(int, lines[N+1].split()))
        B = list(map(int, lines[N+2].split()))

        # Fixing everything
        C = [[int(matrix_C[i][j]) for j in range(M)] for i in range(N)]
        a = A.copy()
        b = B.copy()
        sum_A = sum(a)
        sum_B = sum(b)

        if sum_A != sum_B:
            if sum_A < sum_B:
                # Add Phantom store
                self.is_phantom_store = True
                a.append(sum_B - sum_A)

                # We are Phantom Matrices and we will steal your Vector
                phantom = [[0] * M]
                C.extend(phantom)
            else:
                # Add Phantom store
                # Add Phantom storage
                self.is_phantom_storage = True
                b.append(sum_A - sum_B)

                # We are Phantom Matrices and we will steal your Vector
                phantom = [[0] for _ in range(N)]
                for row in C:
                    row.extend(phantom[0])

        try:
            return TransportTask(C, a, b)
        except Exception as ex:
            raise ex

    def retrieve_correct_answer(self, x):
        if self.is_phantom_store:
            new_x = [row[:-1] for row in x[:-1]]
            x = new_x

        if self.is_phantom_storage:
            new_x = [row[:-1] for row in x]
            x = new_x
        print(x)
