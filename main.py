from TaskLoader import TaskLoader

if __name__ == "__main__":
    t = TaskLoader()
    task = t.load("14.txt")

    # Indices that are the same for potentials for the extreme point
    # HOOOORAY
    #v = task.build_potentials([[0, 0], [1, 0], [2, 1], [2, 2], [3, 3], [1, 4], [3, 4], [0, 1]])

    # Solve with the extreme points method
    print("Extreme point method:")
    try:
        t.retrieve_correct_answer(task.extreme_point_method()).print()
    except Exception as ex:
        print(ex)

    print("\nPotentials method:")
    try:
        t.retrieve_correct_answer(task.PotentialMethod()).print()
    except Exception as ex:
        print(ex)