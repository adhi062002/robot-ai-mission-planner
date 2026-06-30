import json
import os

from ament_index_python.packages import get_package_share_directory


class MissionExecutor:

    def execute(self, mission):

        print("\n========== Mission Executor ==========")

        action = mission["actions"][0]

        package_share = get_package_share_directory(
            "robot_ai_mission_planner"
        )

        filename = os.path.join(
            package_share,
            "missions",
            f"{action['route']}.json"
        )

        try:
            with open(filename) as f:
                route = json.load(f)

        except FileNotFoundError:
            print(f"\n[ERROR] Route file not found: {filename}")
            return

        except json.JSONDecodeError:
            print(f"\n[ERROR] Invalid JSON in: {filename}")
            return

        print("--------------------------------------")
        print(f"Route : {route['name']}")
        print(f"Laps  : {action['laps']}")
        print(f"Speed : {action['speed']}")
        print("--------------------------------------")
        print("\nWaypoints")

        for waypoint in route["waypoints"]:
            print(waypoint)

        print("\nMission Complete")