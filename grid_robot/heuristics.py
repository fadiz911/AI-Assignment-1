import heapq
import math


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    return heuristic


def advanced_heuristic(_grid_robot_state):
    distance = base_heuristic(_grid_robot_state)
    penalty = distance * _grid_robot_state.get_carried_stairs()
    return distance + penalty + 1 / max(1, _grid_robot_state.get_lamp_height() - _grid_robot_state.get_carried_stairs())
