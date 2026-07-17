import os

from ament_index_python.packages import get_package_share_directory

from robot_ai_mission_planner.interfaces.mission_schema import MISSION_SCHEMA


class MissionValidator:

    VALID_MISSIONS = [
        "navigation"
    ]

    VALID_ACTIONS = [
        "follow_route"
    ]

    def __init__(self):
        self.mission_dir = os.path.join(
            get_package_share_directory("robot_ai_mission_planner"),
            "missions"
        )

    def get_valid_routes(self):
        """Scan the missions directory and return route names from saved JSON files."""
        if not os.path.isdir(self.mission_dir):
            return []

        routes = []

        for filename in os.listdir(self.mission_dir):
            if filename.endswith(".json"):
                routes.append(filename[:-len(".json")])

        return routes

    def validate(self, mission):

        valid_routes = self.get_valid_routes()

        # Mission should not be None
        if mission is None:
            print("[ERROR] Mission is None")
            return False

        # LLM returned an error
        if "error" in mission:
            print(f"[ERROR] {mission['error']}")
            return False

        # Check top-level schema
        for key in MISSION_SCHEMA:
            if key not in mission:
                print(f"[ERROR] Missing key: {key}")
                return False
            if not isinstance(mission[key], MISSION_SCHEMA[key]):
                print(f"[ERROR] Invalid type for: {key}")
                return False

        # Mission type
        if mission["mission"] not in self.VALID_MISSIONS:
            print("[ERROR] Unsupported mission type")
            return False

        # At least one action
        if len(mission["actions"]) == 0:
            print("[ERROR] No actions found")
            return False

        # Validate every action
        for action in mission["actions"]:
            required = [
                "type",
                "route",
                "laps",
                "speed"
            ]

            for key in required:
                if key not in action:
                    print(f"[ERROR] Missing action key: {key}")
                    return False

            if action["type"] not in self.VALID_ACTIONS:
                print(f"[ERROR] Unsupported action: {action['type']}")
                return False

            if action["route"] not in valid_routes:
                print(f"[ERROR] Unsupported route: {action['route']}")
                if valid_routes:
                    print(f"[INFO] Available routes: {', '.join(valid_routes)}")
                else:
                    print("[INFO] No recorded missions found in missions directory")
                return False

            if not isinstance(action["laps"], int):
                print("[ERROR] laps must be an integer")
                return False

            if action["laps"] <= 0:
                print("[ERROR] laps must be greater than zero")
                return False

            if not isinstance(action["speed"], (int, float)):
                print("[ERROR] speed must be numeric")
                return False

            if action["speed"] < 0.1 or action["speed"] > 1.0:
                print("[ERROR] speed must be between 0.1 and 1.0 m/s")
                return False

        return True