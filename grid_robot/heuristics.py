import math

from grid_robot_state import grid_robot_state

def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    return math.sqrt((robot_location[0] - lamp_location[0])**2 +(robot_location[1] - lamp_location[1])**2)

def advanced_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    lamp_height = _grid_robot_state.get_location_value(lamp_location)

    carried_stairs = _grid_robot_state.get_carried_stairs()

    stairs_locations = [
        (x, y, _grid_robot_state.get_location_value((x, y)))
        for x in range(len(_grid_robot_state.map))
        for y in range(len(_grid_robot_state.map[0]))
        if _grid_robot_state.get_location_value((x, y)) > 0
    ]

    # Manhattan distance to the lamp
    distance_to_lamp = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])

    # Total stairs height needed
    remaining_stairs_height = max(0, lamp_height - carried_stairs)

    # Calculate the cost of gathering remaining stairs
    stairs_costs = [
        (abs(robot_location[0] - stair[0]) + abs(robot_location[1] - stair[1]) + 1, stair[2])  # +1 for pickup
        for stair in stairs_locations
    ]
    stairs_costs.sort()

    gathering_cost = 0
    for cost, height in stairs_costs:
        if remaining_stairs_height <= 0:
            break
        remaining_stairs_height -= height
        gathering_cost += cost

    # Final cost includes moving to the lamp and gathering stairs
    total_cost = distance_to_lamp + gathering_cost

    return total_cost
