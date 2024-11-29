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
    remaining_stairs_height = max(0, lamp_height - carried_stairs)

    # --- Precompute available stairs ---
    stairs_costs = []
    for x in range(len(_grid_robot_state.map)):
        for y in range(len(_grid_robot_state.map[0])):
            stair_height = _grid_robot_state.get_location_value((x, y))
            if stair_height > 0:
                distance_to_stair = abs(robot_location[0] - x) + abs(robot_location[1] - y)
                heapq.heappush(stairs_costs, (distance_to_stair + 1, stair_height))  # +1 for pickup cost

    # --- Calculate gathering cost using a heap ---
    gathering_cost = 0
    while remaining_stairs_height > 0 and stairs_costs:
        cost, height = heapq.heappop(stairs_costs)
        remaining_stairs_height -= height
        gathering_cost += cost

    # --- Distance to the lamp ---
    distance_to_lamp = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])

    # --- Carrying penalty ---
    carrying_penalty = carried_stairs * distance_to_lamp

    # --- Reflected adjustment ---
    horizontal_cost = abs(robot_location[0] - lamp_location[0])
    vertical_cost = abs(robot_location[1] - lamp_location[1])
    reflected_cost = min(horizontal_cost, vertical_cost)

    # --- Total heuristic cost ---
    total_cost = gathering_cost + carrying_penalty + reflected_cost
    return total_cost