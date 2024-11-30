import heapq
import math


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    del robot_location ,lamp_location
    return heuristic


def advanced_heuristic(_grid_robot_state):
    # Extract robot and lamp coordinates
    robot_x, robot_y = _grid_robot_state.robot_location
    lamp_x, lamp_y = _grid_robot_state.lamp_location
    carried_stairs = _grid_robot_state.carried_stairs
    lamp_height = _grid_robot_state.lamp_height

    # Precompute deltas
    dx = abs(robot_x - lamp_x)
    dy = abs(robot_y - lamp_y)

    # Direct Manhattan distance
    direct_distance = dx + dy

    # Reflected coordinates and distances
    reflected_x = 2 * lamp_x - robot_x
    reflected_y = 2 * lamp_y - robot_y
    reflected_distance = min(
        abs(reflected_x - robot_x) + dy,
        dx + abs(reflected_y - robot_y)
    )

    # Height mismatch penalty without exponentiation
    height_penalty = (lamp_height - carried_stairs) * 1.5 if lamp_height > carried_stairs else 0

    # Closeness reward simplified
    proximity_reward = 5 / (1 + direct_distance + reflected_distance)

    # Combine heuristic components
    return direct_distance + 0.75 * reflected_distance + height_penalty - proximity_reward

