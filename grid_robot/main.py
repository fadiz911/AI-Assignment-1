import time
import tracemalloc
from heuristics import *
from search import *

def get_memory_usage():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    return top_stats[0].size  # Get the largest memory allocation

if __name__ == '__main__':
    map = [[0, 0, 0, 0, 0, 0, 0, 0], [2, 0, -1, 0, 0, 1, 0, 0], [0, -1, 1, 0, 2, 0, -1, 0], [0, 0, 2, 0, -1, 1, 0, 0], [0, 0, 2, 1, 0, 3, 0, 0], [-1, 1, 0, -1, 0, -1, 0, 0], [-1, 0, -1, 0, 0, 1, 0, -1], [0, 0, 0, 0, 0, 0, 0, 0]]
    robot_start_location = (7, 0)
    lamp_h = 4
    lamp_location = (0, 4)

    start_state = grid_robot_state(map=map, robot_location=robot_start_location, lamp_height=lamp_h,
                                   lamp_location=lamp_location)

    # Start tracing memory
    tracemalloc.start()
    start_time = time.time()
    search_result = search(start_state, advanced_heuristic)
    end_time = time.time() - start_time

    # Stop tracing memory and take a snapshot
    memory_after = get_memory_usage()

    # Print runtime and memory usage
    print(f"Runtime: {end_time:.4f} seconds")
    print(f"Memory usage: {memory_after} bytes")

    # Solution cost
    if search_result:
        print(f"Solution cost: {search_result[-1].g}")
        for node in search_result:
            state = node.state  # Extract grid_robot_state
            print(f"State: {state.robot_location}, g: {node.g}, h: {node.h}, f: {node.f}")
    else:
        print("No solution found.")
