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
    lamp_height = _grid_robot_state.get_location_value(lamp_location)

    carried_stairs = _grid_robot_state.get_carried_stairs()

    # List of all available stairs (location and height)
    stairs_locations = [
        (x, y, _grid_robot_state.get_location_value((x, y)))
        for x in range(len(_grid_robot_state.map))
        for y in range(len(_grid_robot_state.map[0]))
        if _grid_robot_state.get_location_value((x, y)) > 0
    ]

    # Distance to lamp (Manhattan distance)
    distance_to_lamp = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])

    # Remaining height required at the lamp
    remaining_stairs_height = max(0, lamp_height - carried_stairs)

    # Calculate cost to gather sufficient stairs
    stairs_costs = []
    for stair in stairs_locations:
        distance_to_stair = abs(robot_location[0] - stair[0]) + abs(robot_location[1] - stair[1])
        stairs_costs.append((distance_to_stair + 1, stair[2]))  # +1 for the pickup cost

    stairs_costs.sort(key=lambda x: x[0])  # Sort by distance

    gathering_cost = 0
    for cost, height in stairs_costs:
        if remaining_stairs_height <= 0:
            break
        remaining_stairs_height -= height
        gathering_cost += cost

    # Add penalty for carrying stairs while moving to the lamp
    carrying_penalty = carried_stairs * distance_to_lamp

    # Total heuristic cost
    total_cost = gathering_cost + carrying_penalty
    return total_cost