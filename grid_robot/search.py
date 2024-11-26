import heapq
from grid_robot_state import grid_robot_state
from search_node import search_node

def create_open_set():
    return []  # Min-heap for the open set

def create_closed_set():
    return set()

def open_not_empty(open_set):
    return len(open_set) != 0

def add_to_open(vn, open_set, best_g):
    state_tuple = vn.state.get_state_tuple()
    # Check if the state is already in best_g and whether the new g is better
    if state_tuple in best_g and best_g[state_tuple] <= vn.g:
        return  # Don't add if a better or equal path already exists

    # Update best_g with the new, better g value
    best_g[state_tuple] = vn.g
    heapq.heappush(open_set, (vn.f, vn.h, vn.g, vn))

def get_best(open_set):
    return heapq.heappop(open_set)[3]  # Extract the node (vn) from the tuple

def add_to_closed(vn, closed_set):
    # Include robot location, stairs carried, and lamp location value
    closed_set.add((
        vn.state.get_state_str(),
        vn.state.get_carried_stairs(),
        vn.state.get_location_value(vn.state.get_lamp_location())
    ))


def duplicate_in_open(vn, open_set):
    # Check if the state is already in open_set with the same number of stairs carried
    state_str = vn.state.get_state_str()
    stairs_carried = vn.state.get_carried_stairs()
    return any(state_str == node.state.get_state_str() and stairs_carried == node.state.get_carried_stairs()
               for _, _, _, node in open_set)

def duplicate_in_closed(vn, closed_set):
    # Check if the state and stairs carried are already in the closed set
    state_str = vn.state.get_state_str()
    stairs_carried = vn.state.get_carried_stairs()
    return (state_str, stairs_carried) in closed_set

def print_path(path):
    for i in range(len(path) - 1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(f"[{path[-1].state.get_state_str()}]")

def search(start_state, heuristic):
    open_set = create_open_set()
    closed_set = create_closed_set()
    best_g = {}  # Track the best g value for each state

    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set, best_g)

    while open_not_empty(open_set):
        current = get_best(open_set)

        if start_state.is_goal_state(current.state):
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            print_path(path)
            return path

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set, best_g)

    print("No solution found.")
    return None
