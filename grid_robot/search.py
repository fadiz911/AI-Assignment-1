import heapq
from search_node import search_node


def create_open_set():
    return []  # Min-heap for the open set


def create_closed_set():
    return set()


def open_not_empty(open_set):
    return bool(open_set)


def add_to_open(vn, open_set):
    heapq.heappush(open_set, vn)


def get_best(open_set):
    return heapq.heappop(open_set)


def add_to_closed(vn, closed_set):
    # Include robot location, stairs carried, and lamp location value
    closed_set.add((
        vn.state.get_robot_location(),
        vn.state.get_carried_stairs(),
        vn.state.get_location_value(vn.state.get_robot_location())
    ))


def duplicate_in_open(vn, open_set):
    # Check if the state is already in open_set with the same number of stairs carried
    state_robot = vn.state.get_robot_location()
    stairs_carried = vn.state.get_carried_stairs()
    return any(state_robot == node.state.get_robot_location() and stairs_carried == node.state.get_carried_stairs()
               for node in open_set)


def duplicate_in_closed(vn, closed_set):
    return (vn.state.get_robot_location(),
            vn.state.get_carried_stairs(),
            vn.state.get_location_value(vn.state.get_robot_location())
            ) in closed_set


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

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)

    return None
