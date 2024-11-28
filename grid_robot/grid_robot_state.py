import copy


class grid_robot_state:
    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1), carried_stairs=0):
        self.robot_location = robot_location
        self.lamp_height = lamp_height
        self.lamp_location = lamp_location
        self.carried_stairs = carried_stairs

        if map is not None:
            if isinstance(map, dict):  # If the map is already compressed
                self.map = map
                self.height = max(k[0] for k in map.keys()) + 1 if map else 0
                self.width = max(k[1] for k in map.keys()) + 1 if map else 0
            else:  # map is a 2D list
                self.height = len(map)
                self.width = len(map[0])
                self.map = {
                    (r, c): map[r][c]
                    for r in range(self.height)
                    for c in range(self.width)
                    if map[r][c] != 0
                }
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
            self.robot_location,
            self.carried_stairs,
            self.lamp_location,
            self.lamp_height,
            tuple(sorted(self.map.items())),
        )

    def get_neighbors(self):
        neighbors = []
        x, y = self.robot_location
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # Raise Stairs by Robot
        if self.carried_stairs == 0 and self.get_location_value(self.robot_location) > 0:
            location = self.robot_location
            stairs_at_location = self.get_location_value(location)
            new_map = copy.copy(self.map)
            new_map.pop(location) # Remove stairs from current location
            new_state = grid_robot_state(
                robot_location=self.robot_location,
                map=new_map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                carried_stairs=stairs_at_location
            )
            neighbors.append((new_state, 1))

        # Place Stairs by Robot
        if self.carried_stairs > 0 and self.get_location_value(self.robot_location) == 0:
            new_map = copy.copy(self.map)
            loc = (x, y)
            new_map[loc] = self.carried_stairs  # Place stairs at current location
            new_state = grid_robot_state(
                robot_location=self.robot_location,
                map=new_map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                carried_stairs=0
            )
            neighbors.append((new_state, 1))

        # Connect Stairs by Robot
        if self.carried_stairs > 0 and self.get_location_value(self.robot_location) > 0:
            combined_height = self.carried_stairs + self.get_location_value(self.robot_location)
            if combined_height <= self.get_lamp_height():
                new_map = copy.copy(self.map)
                new_map.pop((x,y))  # Remove stairs from the map
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
            if 0 <= new_x < self.height and 0 <= new_y < self.width:
                if self.map.get((new_x, new_y), 0) != -1:  # Ensure the new space is not an obstacle
                    cost = 1 + self.carried_stairs  # Additional cost if carrying stairs
                    new_state = grid_robot_state(
                        robot_location=(new_x, new_y),
                        map=copy.copy(self.map),
                        lamp_height=self.lamp_height,
                        lamp_location=self.lamp_location,
                        carried_stairs=self.carried_stairs
                    )
                    neighbors.append((new_state, cost))

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
        return self.map.get(location, 0)

    def set_location_value(self, location, val):
        if val > 0:
            self.map[location] = val
        elif location in self.map:
            del self.map[location]

    def get_robot_location(self):
        return self.robot_location
