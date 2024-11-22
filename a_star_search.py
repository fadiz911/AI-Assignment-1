from queue import PriorityQueue
#test
import pandas as pd

# The function initializes and returns open
def init_open():
    return PriorityQueue()

# The function inserts s into open
def insert_to_open(open_list, s):  # Should be implemented according to the open list data structure
    open_list.append(s)


# The function returns the best node in open (according to the search algorithm)
def get_best(open_list):
    return open_list.

# The function returns neighboring locations of s_location
def get_neighbors(grid, s_location):
    # neighbors = []
    raise NotImplementedError
    # return neighbors

# The function returns whether or not s_location is the goal location
def is_goal(s_location, goal_location):
    if s_location == goal_location:
    raise NotImplementedError

# The function estimates the cost to get from s_location to goal_location
def calculate_heuristic(s_location, goal_location):
    raise NotImplementedError

# The function returns whether n_location should be generated (checks in open_list)
# removes a node from open_list if needed 
def check_for_duplicates_open(n_location, s, open_list):
    raise NotImplementedError
  
  
# The function returns whether n_location should be generated (checks in closed_list)
# removes a node from closed_list if needed  
def check_for_duplicates_close(n_location, s, closed_list):
    raise NotImplementedError
    
    
# Locations are tuples of (x, y)
def astar_search(grid, start_location, goal_location):
    # State = (f, h, g, x, y, s_prev) # f = g + h (For Priority Queue)
    # Start_state = (0, 0, 0, x_0, y_0, False)
    start = (0, 0, 0, start_location[0], start_location[1], False)
    open_list = init_open()
    closed_list = {}
    # Mark the source node as
    # visited and enqueue it
    insert_to_open(open_list, start)
    while not open_list.empty():
        # Dequeue a vertex from
        # queue and print it
        s = get_best(open_list)
        s_location = (s[3], s[4])
        if s_location in closed_list:
            continue
        if is_goal(s_location, goal_location):
            print("The number of states visited by AStar Search:", len(closed_list))
            return s
        neighbors_locations = get_neighbors(grid, s_location)
        for n_location in neighbors_locations:
            if check_for_duplicates_open(n_location, s, open_list) or check_for_duplicates_close(n_location, s, closed_list):
                continue
            h = calculate_heuristic(n_location, goal_location)
            g = s[2] + 1
            f = g + h
            n = (f, h, g, n_location[0], n_location[1], s)
            insert_to_open(open_list, n)
        closed_list[s_location] = s

def print_route(s):
    for r in s:
        print(r)

def get_route(s):
    route = []
    while s:
        s_location = (s[3], s[4])
        route.append(s_location)
        s = s[5]
    route.reverse()
    return route

def print_grid_route(route, grid):
    for location in route:
        grid[location] = 'x'
    print(pd.DataFrame(grid))
