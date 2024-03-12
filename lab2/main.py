import copy

from TaskLoader import TaskLoader

if __name__ == "__main__":
    t = TaskLoader()
    task = t.load("14.txt")

    vector_sol = []
    # Solve with the extreme points method
    print("Extreme point method:")
    try:
        x_sol, vector_sol = task.extreme_point_method()
        print(vector_sol)
        t.retrieve_correct_answer(x_sol)
    except Exception as ex:
        print(ex)

    print("\nPotentials method:")
    try:
        sol_potentional = task.MethodPotentional()
        solution = []
        for row in sol_potentional:
            solution += row

        print("Solution in vector solution of extreme point method", solution in vector_sol)
        t.retrieve_correct_answer(sol_potentional)
    except Exception as ex:
        print(ex)
