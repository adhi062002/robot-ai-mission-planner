import json

from src.interfaces.ros2_interface import ROS2Interface


class MissionExecutor:

    def __init__(self):

        self.robot = ROS2Interface()

    def execute(self, mission):

        print("\n===== EXECUTING MISSION =====")

        action = mission["actions"][0]

        filename = f"missions/{action['route']}.json"

        with open(filename) as f:

            route = json.load(f)

        self.robot.follow_route(

            route,

            action["laps"],

            action["speed"]

        )

        print("\nMission Complete")

        
        self.robot.shutdown()