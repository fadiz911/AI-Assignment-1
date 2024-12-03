import copy


class grid_robot_state:
    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1), carried_stairs=0):
        self.robot_location = robot_location
        if map is not None:
            if isinstance(map, dict):  # If the map is already compressed
                self.map = map
                self.height = max(k[0] for k in map.keys()) + 1 if map else 0
                self.width = max(k[1] for k in map.keys()) + 1 if map else 0
            else:  # map is a 2D list
                self.height = len(map)
                self.width = len(map[0])
                self.map = {(r, c): map[r][c] for r, row in enumerate(map) for c, val in enumerate(row) if val}
        self.obstacles = [key for key in self.map.keys() if self.map[key] == -1]
        self.lamp_height = lamp_height
        self.lamp_location = lamp_location
        self.carried_stairs = carried_stairs

    @staticmethod
    def is_goal_state(_grid_robot_state):
        robot_location = _grid_robot_state.robot_location
        lamp_location = _grid_robot_state.lamp_location

        # Check if robot is at the lamp location
        if robot_location != lamp_location:
            return False

        # Check if the height at the lamp location matches the lamp height
        return _grid_robot_state.get_location_value(lamp_location) == _grid_robot_state.get_lamp_height()

    def get_state_tuple(self):
        return (
            hash(self.robot_location),
            self.carried_stairs,
            self.lamp_location,
            self.lamp_height,
            hash(frozenset(self.map.items()))  # Convert map to a tuple of tuples
        )

    def get_neighbors(self):
        neighbors = []
        x, y = self.robot_location
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        original_value = self.get_location_value(self.robot_location)

        # Raise Stairs by Robot
        if self.carried_stairs == 0 and original_value > 0:
            stairs_at_location = original_value
            new_map = copy.copy(self.map)
            del new_map[(x,y)]
            new_state = grid_robot_state(
                robot_location=self.robot_location,
                map=new_map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                carried_stairs=stairs_at_location
            )
            neighbors.append((new_state, 1))  # Cost is 1 for lifting stairs

        # Place Stairs by Robot
        elif self.carried_stairs > 0 and original_value == 0:
            new_map = copy.copy(self.map)
            new_map[(x,y)] = self.carried_stairs  # Place stairs at the current location
            new_state = grid_robot_state(
                robot_location=self.robot_location,
                map=new_map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                carried_stairs=0
            )
            neighbors.append((new_state, 1))  # Cost is 1 for placing stairs

        # Connect Stairs by Robot
        elif self.carried_stairs > 0 and original_value > 0:
            combined_height = self.carried_stairs + original_value
            if combined_height <= self.get_lamp_height():
                new_map = copy.copy(self.map)
                del new_map[(x,y)]
                new_state = grid_robot_state(
                    robot_location=self.robot_location,
                    map=new_map,
                    lamp_height=self.lamp_height,
                    lamp_location=self.lamp_location,
                    carried_stairs=combined_height
                )
                neighbors.append((new_state, 1))  # Cost is 1 for connecting stairs

        # Move Robot
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < self.height and 0 <= new_y < self.width and self.map.get((new_x,new_y),0) != -1:
                move_cost = 1 + self.carried_stairs
                new_state = grid_robot_state(
                    robot_location=(new_x, new_y),
                    map=self.map,  # Reuse original map
                    lamp_height=self.lamp_height,
                    lamp_location=self.lamp_location,
                    carried_stairs=self.carried_stairs
                )
                neighbors.append((new_state, move_cost))
        return neighbors

    def get_carried_stairs(self):
        return self.carried_stairs

    def get_state_str(self):
        return str(self.robot_location)

    def get_lamp_location(self):
        return self.lamp_location

    def get_lamp_height(self):
        return self.lamp_height

    def get_location_value(self, location):
        return self.map.get(location,0)

    def set_location_value(self, location, val):
        self.map[location[0]][location[1]] += val

    def get_robot_location(self):
        return self.robot_location

    def __hash__(self):
        return hash(self.get_state_tuple())