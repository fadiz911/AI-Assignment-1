import heapq
from grid_robot_state import grid_robot_state
from search_node import search_node

def create_open_set():
    open =[]
    hash_open = {}
    return (open,hash_open)  # Min-heap for the open set

def create_closed_set():
    hash_closed = {}
    return hash_closed

def open_not_empty(open_set):
    return len(open_set[0])>0

def get_best(open_set):
    vn = heapq.heappop(open_set[0])
    while len(open_set[0])>0 and(hash(vn.state)) not in open_set[1] or vn != open_set[1][hash(vn.state)]:
        vn = heapq.heappop(open_set[0])
    del open_set[1][hash(vn.state)]
    return vn


def add_to_open(vn, open_set):
    heapq.heappush(open_set[0], vn)
    open_set[1][hash(vn.state)]= vn


def add_to_closed(vn, closed_set):
    closed_set[hash(vn.state)] = vn

def duplicate_in_open(vn, open_set):
    if hash(vn.state) not in open_set[1]:
        return False
    if open_set[1][hash(vn.state)].g <=vn.g: return True
    del open_set[1][hash(vn.state)]
    return False

def duplicate_in_closed(vn, closed_set):
   if hash(vn.state) not in closed_set:return False
   if closed_set[1][hash(vn.state)].g <= vn.g:return True
   del closed_set[1][hash(vn.state)]
   return False

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