import math

from grid_robot_state import grid_robot_state


#test


def base_heuristic(_grid_robot_state):
    robot_location = grid_robot_state.get_robot_location()
    lamp_location = grid_robot_state.get_lamp_location()
    return math.sqrt((robot_location[0] - lamp_location[0])**2 +(robot_location[1] - lamp_location[1])**2)


def advanced_heuristic(_grid_robot_state):
    return 0
