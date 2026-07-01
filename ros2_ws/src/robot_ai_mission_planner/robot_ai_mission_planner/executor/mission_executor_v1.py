import json
import os

from ament_index_python.packages import get_package_share_directory


class MissionExecutor:

    def execute(self, mission):

        print("\n========== Mission Executor ==========")

        for action in mission["actions"]:

            if action["type"] == "follow_route":

                route = self.load_route(action["route"])

                if route is None:
                    continue

                print("--------------------------------------")
                print(f"Route : {route['name']}")
                print(f"Laps  : {action['laps']}")
                print(f"Speed : {action['speed']}")
                print("--------------------------------------")

                print("\nWaypoints\n")

                for index, waypoint in enumerate(route["waypoints"], start=1):

                    print(
                        f"Navigating to Waypoint {index}: "
                        f"x={waypoint[0]}, y={waypoint[1]}"
                    )

                    # Placeholder for Nav2
                    print("Goal reached\n")

            else:

                print(f"\n[WARNING] Unknown action: {action['type']}")

        print("\nMission Complete")

    def load_route(self, route_name):

        package_share = get_package_share_directory(
            "robot_ai_mission_planner"
        )

        filename = os.path.join(
            package_share,
            "missions",
            f"{route_name}.json"
        )

        try:

            with open(filename) as f:
                return json.load(f)

        except FileNotFoundError:

            print(f"\n[ERROR] Route file not found: {filename}")
            return None

        except json.JSONDecodeError:

            print(f"\n[ERROR] Invalid JSON in: {filename}")
            return None