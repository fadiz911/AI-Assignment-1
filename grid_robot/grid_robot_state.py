class grid_robot_state:
    # you can add global params
    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1), carried_stairs=0):
        self.robot_location = robot_location
        self.map = map
        self.lamp_height = lamp_height
        self.lamp_location = lamp_location
        self.carried_stairs = carried_stairs  # Add carried_stairs as a parameter

    @staticmethod
    def is_goal_state(_grid_robot_state):
        robot_location = _grid_robot_state.robot_location
        lamp_location = _grid_robot_state.lamp_location
        return robot_location[0] == lamp_location[0] and robot_location[1] == lamp_location[
            1] and _grid_robot_state.get_lamp_height() == _grid_robot_state.get_carried_stairs()

    def get_neighbors(self):
        neighbors = []
        x, y = self.robot_location
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        #  move from one location to another
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(self.map) and 0 <= new_y < len(self.map[0]):
                if self.map[new_x][new_y] != -1:
                    cost = 1
                    if self.lamp_height > 0:
                        cost += self.lamp_height
                    new_state = grid_robot_state(
                        robot_location=(new_x, new_y),
                        map=self.map,
                        lamp_height=self.lamp_height,
                        lamp_location=self.lamp_location
                    )
                    neighbors.append((new_state, cost))

        # putting stairs
        if self.carried_stairs == 0 and self.get_location_value(self.robot_location) > 0:
            new_state = grid_robot_state(
                robot_location=self.robot_location,
                map=self.map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                carried_stairs=self.get_location_value(self.robot_location)
            )
            neighbors.append((new_state, 1))

        # getting stairs
        if self.carried_stairs > 0 and self.get_location_value(self.robot_location) == 0:
            new_map = [row[:] for row in self.map]
            new_map[x][y] = self.carried_stairs
            new_state = grid_robot_state(
                robot_location=self.robot_location,
                map=new_map,
                lamp_height=self.lamp_height,
                lamp_location=self.lamp_location,
                carried_stairs=0
            )
            neighbors.append((new_state, 1))

        # adding stairs to existing ones
        if self.lamp_height > 0 and self.get_location_value(self.robot_location) > 0:
            combined_height = self.lamp_height + self.get_location_value(self.robot_location)
            if combined_height <= self.get_location_value(self.lamp_location):
                new_map = [row[:] for row in self.map]
                new_map[x][y] = combined_height
                new_state = grid_robot_state(
                    robot_location=self.robot_location,
                    map=new_map,
                    lamp_height=-1,
                    lamp_location=self.lamp_location
                )
                neighbors.append((new_state, 1))

        return neighbors

    def get_carried_stairs(self):
        return self.carried_stairs

    def get_state_str(self):
        return self.robot_location

    #you can add helper functions

    def get_lamp_location(self):
        return self.lamp_location

    def get_lamp_height(self):
        return self.lamp_height

    def get_location_value(self, location):
        return self.map[location[0]][location[1]]

    def get_robot_location(self):
        return self.robot_location
