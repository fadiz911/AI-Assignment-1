import time
from heuristics import *
from search import *

if __name__ == '__main__':
    map = [
        [0, 0, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0],
        [2, 0, -1, -1, 0, 1, 0, -1, 2, 0, -1, 0],
        [0, -1, 1, 0, 2, 0, -1, 0, -1, 0, 3, 0],
        [0, 0, 2, -1, -1, 1, 0, 0, -1, 0, 0, 0],
        [0, 0, 2, 1, 0, 3, -1, 0, 2, 1, 0, -1],
        [-1, 1, 0, -1, 0, -1, 0, -1, 0, 0, 1, 0],
        [-1, 0, -1, 0, 0, 1, 0, 0, -1, 0, -1, 0],
        [0, 0, 0, 0, 0, 0, 2, 1, 0, -1, 0, 0],
        [2, -1, 0, -1, 3, 0, 0, -1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0, -1, 0, 0],
        [-1, 0, 0, -1, 0, 2, 0, 3, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0, 0],
    ]

    robot_start_location = (11, 0)
    lamp_h = 6
    lamp_location = (0, 11)

    # Proceed with the search
    start_state = grid_robot_state(map=map, robot_location=robot_start_location, lamp_height=lamp_h,
                                   lamp_location=lamp_location)
    start_time = time.time()
    search_result = search(start_state, advanced_heuristic)
    end_time = time.time() - start_time

    # Runtime
    print(f"Runtime: {end_time:.2f} seconds")

    # Solution cost
    if search_result:
        print(f"Solution cost: {search_result[-1].g}")
        for node in search_result:
            state = node.state  # Extract grid_robot_state
            print(f"State: {state.robot_location}, g: {node.g}, h: {node.h}, f: {node.f}")
    else:
        print("No solution found.")
