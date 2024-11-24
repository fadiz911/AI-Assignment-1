class grid_robot_state:
    # you can add global params

    def __init__(self, robot_location, map=None, lamp_height=-1, lamp_location=(-1, -1)):
        # you can use the init function for several purposes
        self.robot_location = robot_location
        self.map = map
        self.lamp_height = lamp_height
        self.lamp_location = lamp_location

    @staticmethod
    def is_goal_state(_grid_robot_state):
        robot_location = _grid_robot_state.robot_location
        lamp_location = _grid_robot_state.lamp_location
        return robot_location[0] == lamp_location[0] and robot_location[1] == lamp_location[1] and grid_robot_state.get_lamp_height() == grid_robot_state.get_location_value(lamp_location)


    def get_neighbors(self):
        pass

        # you can change the body of the function if you want
        # def __hash__(self):

        # you can change the body of the function if you want
        # def __eq__(self, other):
        # you can change the body of the function if you want

    def get_state_str(self):
        return self.location



    #you can add helper functions

    def get_lamp_location(self):
        return self.lamp_location

    def get_lamp_height(self):
        return self.lamp_height

    def get_location_value(self,location):
        return self.map[location[0]][location[1]]

    def get_robot_location(self):
        return self.robot_location