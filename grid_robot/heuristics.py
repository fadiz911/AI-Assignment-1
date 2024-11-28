import heapq
import math
from grid_robot_state import grid_robot_state


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    return heuristic


def advanced_heuristic(_grid_robot_state):
    """
    A heuristic combining the Manhattan distance to the lamp and the effort
    to gather sufficient stairs to match the lamp height.
    """
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    lamp_height = _grid_robot_state.get_lamp_height()
    carried_stairs = _grid_robot_state.get_carried_stairs()

    # Remaining height needed at the lamp
    remaining_height = max(0, lamp_height - carried_stairs)

    # Distance from robot to lamp (Manhattan distance)
    distance_to_lamp = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])

    # If no remaining height is needed, the cost is just the distance to the lamp
    if remaining_height == 0:
        return distance_to_lamp

    # Gather all stairs locations and heights
    stairs_locations = [
        (x, y, height)
        for (x, y), height in _grid_robot_state.map.items()
        if height > 0
    ]

    # If no stairs are available, returning a very high cost
    if not stairs_locations:
        return float('inf')  # No solution if stairs are needed but not available

    # Calculate the minimal cost to gather enough stairs
    stairs_costs = []
    for x, y, height in stairs_locations:
        distance_to_stair = abs(robot_location[0] - x) + abs(robot_location[1] - y)
        stairs_costs.append((distance_to_stair + 1, height))  # +1 for the pickup cost

    # Sort stairs by distance to prioritize closer ones
    stairs_costs.sort(key=lambda x: x[0])

    gathering_cost = 0
    total_gathered_height = carried_stairs

    # Accumulate gathering cost until enough stairs are collected
    for cost, height in stairs_costs:
        if total_gathered_height >= lamp_height:
            break
        total_gathered_height += height
        gathering_cost += cost

    # Remaining penalty for not having enough stairs after visiting all possible sources
    remaining_penalty = max(0, lamp_height - total_gathered_height)

    # Heuristic: gathering cost + distance to lamp + remaining penalty
    return gathering_cost + distance_to_lamp + remaining_penalty

