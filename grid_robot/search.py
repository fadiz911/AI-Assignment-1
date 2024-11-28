import heapq
from grid_robot_state import grid_robot_state
from search_node import search_node

def create_open_set():
    return []  # Min-heap for the open set

def create_closed_set():
    return set()

def open_not_empty(open_set):
    return bool(open_set)

def get_best(open_set):
    return heapq.heappop(open_set)


def add_to_open(vn, open_set):
    """
    Adds a search node to the open set, ensuring no duplicate states with worse or equal `g` values.
    """
    state_tuple = vn.state.get_state_tuple()

    # Iterate through open_set to find duplicates
    for index, node in enumerate(open_set):
        if node.state.get_state_tuple() == state_tuple:
            if node.g <= vn.g:
                return  # If a better or equal `g` value exists, skip adding
            else:
                # Remove the worse node and push the new one
                open_set[index] = open_set[-1]  # Replace with the last element
                open_set.pop()  # Remove the duplicate
                heapq.heappush(open_set, vn)  # Push the new node and restore heap properties
                return

    # Push the new node onto the heap
    heapq.heappush(open_set, vn)


def add_to_closed(vn, closed_set):
    # Include robot location, stairs carried, and lamp location value
    closed_set.add((
        vn.state.get_state_str(),
        vn.state.get_carried_stairs(),
        vn.state.get_location_value(vn.state.get_robot_location())
    ))

def duplicate_in_open(vn, open_set):
    state_tuple = vn.state.get_state_tuple()
    # Check for duplicate in open_set using the state_tuple
    return any(node.state.get_state_tuple() == state_tuple and node.g <= vn.g for node in open_set)

def duplicate_in_closed(vn, closed_set):
    return (vn.state.get_state_str(),
            vn.state.get_carried_stairs(),
            vn.state.get_location_value(vn.state.get_robot_location())
            ) in closed_set

# Helps to debug sometimes..
def print_path(path):
    for i in range(len(path)-1):
        print(f"[{path[i].state.get_state_str()}]", end=", ")
    print(path[-1].state.state_str)


def search(start_state, heuristic):
    open_set = create_open_set()
    closed_set = create_closed_set()
    start_node = search_node(start_state, 0, heuristic(start_state))
    add_to_open(start_node, open_set)

    while open_not_empty(open_set):
        current = get_best(open_set)

        if grid_robot_state.is_goal_state(current.state):
            path = []
            while current:
                path.append(current)
                current = current.prev
            path.reverse()
            return path

        add_to_closed(current, closed_set)

        for neighbor, edge_cost in current.get_neighbors():
            curr_neighbor = search_node(neighbor, current.g + edge_cost, heuristic(neighbor), current)
            if not duplicate_in_open(curr_neighbor, open_set) and not duplicate_in_closed(curr_neighbor, closed_set):
                add_to_open(curr_neighbor, open_set)

    return None
