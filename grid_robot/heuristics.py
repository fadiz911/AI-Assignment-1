import heapq
import math
from grid_robot_state import grid_robot_state


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    return heuristic


def advanced_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    lamp_height = _grid_robot_state.get_lamp_height()
    carried_stairs = _grid_robot_state.get_carried_stairs()

    # Remaining height needed at the lamp
    remaining_height = max(0, lamp_height - carried_stairs)

    # Distance from robot to lamp (Manhattan distance)
    distance_to_lamp = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])

    # If no remaining height is needed, the heuristic is just the distance to the lamp
    if remaining_height == 0:
        return distance_to_lamp

    # Minimal cost to gather enough stairs
    stairs_cost = float('inf')
    for (x, y), height in _grid_robot_state.map.items():
        # Skip locations without stairs
        if height <= 0:
            continue

        # Distance to the stair location
        distance_to_stair = abs(robot_location[0] - x) + abs(robot_location[1] - y)

        # Cost to gather stairs from this location and move to the lamp
        gather_cost = distance_to_stair + 1  # +1 for pickup cost
        stairs_cost = min(stairs_cost, gather_cost)

    # If no stairs are available, return an overestimated value (not admissible)
    if stairs_cost == float('inf'):
        return distance_to_lamp + remaining_height

    # Heuristic is the cost to gather stairs + distance to the lamp
    return stairs_cost + distance_to_lamp
