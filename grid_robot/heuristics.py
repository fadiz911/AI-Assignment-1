import heapq
import math


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    del robot_location ,lamp_location
    return heuristic


def advanced_heuristic(_grid_robot_state):
    # Extract robot and lamp coordinates directly (avoiding creating temporary variables)
    robot_x, robot_y = _grid_robot_state.robot_location
    lamp_x, lamp_y = _grid_robot_state.lamp_location
    carried_stairs = _grid_robot_state.carried_stairs
    lamp_height = _grid_robot_state.lamp_height

    # Precompute deltas (absolute differences)
    dx = abs(robot_x - lamp_x)
    dy = abs(robot_y - lamp_y)

    # Direct Manhattan distance (simplified calculation)
    direct_distance = dx + dy

    # Reflected distance can be skipped since it's the same as direct distance in this case
    reflected_distance = direct_distance

    # Calculate height penalty without extra conditionals
    height_penalty = max(0, lamp_height - carried_stairs)

    # Compute proximity reward with reduced computation
    proximity_reward = max(0, 5 - (direct_distance + reflected_distance))

    # Combine results, using simple addition/subtraction for all terms
    return direct_distance + reflected_distance + height_penalty - proximity_reward
