import heapq
import math
from grid_robot_state import grid_robot_state


def base_heuristic(_grid_robot_state):
    robot_location = _grid_robot_state.get_robot_location()
    lamp_location = _grid_robot_state.get_lamp_location()
    heuristic = abs(robot_location[0] - lamp_location[0]) + abs(robot_location[1] - lamp_location[1])
    del robot_location ,lamp_location
    return heuristic


def advanced_heuristic(_grid_robot_state):
    # Direct attribute access to minimize overhead
    robot_x, robot_y = _grid_robot_state.robot_location
    lamp_x, lamp_y = _grid_robot_state.lamp_location
    lamp_height = _grid_robot_state.lamp_height
    carried_stairs = _grid_robot_state.carried_stairs
    obstacles = _grid_robot_state.obstacles  # Assuming obstacles is a list of (x, y) tuples

    # Manhattan distance calculation (avoiding temporary variables)
    manhattan_distance = abs(robot_x - lamp_x) + abs(robot_y - lamp_y)

    # Height penalty: calculate based on lamp height and carried stairs
    height_penalty = max(lamp_height - carried_stairs, 0)

    # Proximity reward: simple, efficient calculation (2 * Manhattan distance)
    proximity_reward = max(5 - (manhattan_distance * 2), 0)

    # Obstacle penalty calculation: penalize based on obstacles along the direct path
    obstacle_penalty = 0
    for ox, oy in obstacles:
        # Check if obstacle is along the straight line path between robot and lamp
        # We check if the obstacle lies on the line of the Manhattan path
        if (robot_x == lamp_x and robot_y != oy and robot_y < oy < lamp_y or lamp_y < oy < robot_y) or \
           (robot_y == lamp_y and robot_x != ox and robot_x < ox < lamp_x or lamp_x < ox < robot_x):
            obstacle_penalty += 10  # Adjust penalty value for obstacles

    # Final heuristic computation
    return (manhattan_distance * 2) + height_penalty - proximity_reward + obstacle_penalty

