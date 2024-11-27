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

    # Collect all stairs locations and their heights from the compressed map
    stairs_locations = [
        (x, y, height)
        for (x, y), height in _grid_robot_state.map.items()
    ]

    # Distance to the lamp
    distance_to_lamp = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])

    # If no remaining height is needed, the cost is just the distance to the lamp
    if remaining_height == 0:
        return distance_to_lamp

    # Calculate the minimal cost to gather enough stairs
    stairs_costs = []
    for x, y, height in stairs_locations:
        distance_to_stair = abs(robot_location[0] - x) + abs(robot_location[1] - y)
        stairs_costs.append((distance_to_stair + 1, height))  # +1 for the pickup cost

    # Sort stairs by distance to prioritize closer ones
    stairs_costs.sort(key=lambda x: x[0])

    gathering_cost = 0
    total_gathered_height = carried_stairs

    for cost, height in stairs_costs:
        if total_gathered_height >= lamp_height:
            break
        total_gathered_height += height
        gathering_cost += cost

    # Remaining height penalty encourages paths that meet lamp height
    remaining_penalty = max(0, lamp_height - total_gathered_height)

    # Total heuristic: gathering cost + distance to lamp + penalty
    return gathering_cost + distance_to_lamp + remaining_penalty
