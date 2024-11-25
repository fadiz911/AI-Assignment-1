import heapq
from grid_robot_state import grid_robot_state
from search_node import search_node


def create_open_set():
    return []  # Min-heap for the open set


def create_closed_set():
    return set()  # Set for the closed set


def open_not_empty(open_set):
    return len(open_set) != 0


def add_to_open(vn, open_set):
    # Push the node to the heap
    heapq.heappush(open_set, (vn.f, vn))  # Add as a tuple (f-value, node)


def get_best(open_set):
    return heapq.heappop(open_set)[1]  # Return the node with the smallest f-value


def add_to_closed(vn, closed_set):
    # Add a tuple of (state string, stairs carried) to the closed set
    closed_set.add((vn.state.get_state_str(), vn.state.get_carried_stairs()))



def duplicate_in_open(vn, open_set):
    # Check if the state is already in open_set with the same number of stairs carried
    state_str = vn.state.get_state_str()
    stairs_carried = vn.state.get_carried_stairs()
    return any(state_str == node.state.get_state_str() and stairs_carried == node.state.get_carried_stairs()
               for _, node in open_set)


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
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):

        current = get_best(open_set)
        if start_state.is_goal_state(current.state):
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)
        print(f"exploring the neighbors of {current.state.get_state_str()}")
        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)

    return None