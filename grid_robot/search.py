import queue

from search_node import search_node
from grid_robot_state import grid_robot_state


def create_open_set():
    return []


def create_closed_set():
    return set()


def add_to_open(vn, open_set):
    i = 0
    while i < len(open_set):
        if vn < open_set[i]:
            break
        i += 1
    if i >= len(open_set):
        open_set.append(vn)
    else:
        open_set = open_set[:i] + vn + open_set[i + 1:]


def open_not_empty(open_set):
    return len(open_set) != 0


def get_best(open_set):
    return open_set.pop(-1)


def add_to_closed(vn, closed_set):
    closed_set.add(vn)


#returns False if curr_neighbor state not in open_set or has a lower g from the node in open_set
#remove the node with the higher g from open_set (if exists)
def duplicate_in_open(vn, open_set):
    for i in range(0, len(open_set)):
        if vn.state == open_set[i].state:
            if vn < open_set[i]:
                open_set.pop(i)
            else:
                open_set.pop(open_set.index(vn))
    pass


#returns False if curr_neighbor state not in closed_set or has a lower g from the node in closed_set
#remove the node with the higher g from closed_set (if exists)
def duplicate_in_closed(vn, closed_set):
    pass


# helps to debug sometimes..
def print_path(path):
    for i in range(len(path) - 1):
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
