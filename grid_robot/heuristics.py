import heapq
import math


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    del robot_location ,lamp_location
    return heuristic


def advanced_heuristic(_grid_robot_state):
    # Extract values to minimize repeated lookups
    robot_x, robot_y = _grid_robot_state.robot_location
    lamp_x, lamp_y = _grid_robot_state.lamp_location
    carried_stairs = _grid_robot_state.carried_stairs
    lamp_height = _grid_robot_state.lamp_height

    # Precompute reflected coordinates only once
    reflected_x = (2 * lamp_x) - robot_x
    reflected_y = (2 * lamp_y) - robot_y

    # Precompute the distances once
    base_distance = abs(robot_x - lamp_x) + abs(robot_y - lamp_y)
    # Calculate the reflected Manhattan distance (minimized)
    reflected_distance = min(
        abs(reflected_x - robot_x) + abs(lamp_y - robot_y),
        abs(lamp_x - robot_x) + abs(reflected_y - robot_y)
    )

    # Avoid using 'max' by handling conditions directly
    height_penalty = (lamp_height - carried_stairs) * 0.5 if lamp_height > carried_stairs else 0

    # Calculate total penalty
    penalty = carried_stairs * (base_distance + reflected_distance) + height_penalty

    # Return total heuristic
    return base_distance + reflected_distance + penalty
