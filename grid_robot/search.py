import heapq
from grid_robot_state import grid_robot_state
from search_node import search_node



def create_open_set():
    """
    Creates an open set represented as a min-heap for priority queue
    and a dictionary for quick access to nodes by their state hash.
    """
    return [], {}  # Min-heap for priority queue and dictionary for state lookup


def create_closed_set():
    """
    Creates a closed set represented as a dictionary for fast lookup by state hash.
    """
    return {}


def open_not_empty(open_set):
    """
    Checks if the open set (priority queue) is not empty.
    """
    return bool(open_set[0])  # True if the heap contains elements


def get_best(open_set):
    """
    Retrieves and removes the best node (lowest f-score) from the open set.
    Ensures the node exists in the dictionary before returning it.
    """
    return heapq.heappop(open_set[0])
    # min_heap, node_dict = open_set
    # while min_heap:
    #     best_node = heapq.heappop(min_heap)
    #     state_hash = hash(best_node.state)
    #     if state_hash in node_dict and node_dict[state_hash] == best_node:
    #         del node_dict[state_hash]
    #         return best_node
    # return None  # No valid nodes remaining


def add_to_open(vn, open_set):
    """
    Adds a search vn to the open set.
    Updates the dictionary for quick access.
    """
    min_heap, node_dict = open_set
    state_hash = hash(vn.state)
    if state_hash not in node_dict or vn.g < node_dict[state_hash].g:
        node_dict[state_hash] = vn  # Update dictionary with the better node
        heapq.heappush(min_heap, vn)  # Push to the heap



def add_to_closed(vn, closed_set):
    """
    Adds a search vn to the closed set.
    """
    closed_set[hash(vn.state)] = vn


def duplicate_in_open(vn, open_set):
    """
    Checks if a vn is a duplicate in the open set with a lower or equal cost.
    If the current vn is better, it removes the old one from the dictionary.
    """
    state_hash = hash(vn.state)
    node_dict = open_set[1]
    if state_hash in node_dict:
        existing_node = node_dict[state_hash]
        # If the existing node has a lower or equal cost, return True (skip adding)
        if existing_node.g <= vn.g:
            return True
        # Otherwise, replace it (better node found)
        del node_dict[state_hash]
    return False


def duplicate_in_closed(vn, closed_set):
    """
    Checks if a vn is a duplicate in the closed set with a lower or equal cost.
    If the current vn is better, it removes the old one from the closed set.
    """
    state_hash = hash(vn.state)
    if state_hash in closed_set:
        existing_node = closed_set[state_hash]
        if existing_node.g <= vn.g:
            return True
        del closed_set[state_hash]
    return False


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
