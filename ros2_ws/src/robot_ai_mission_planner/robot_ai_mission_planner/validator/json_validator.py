from robot_ai_mission_planner.interfaces.mission_schema import MISSION_SCHEMA


class MissionValidator:

    VALID_MISSIONS = [
        "navigation"
    ]

    VALID_ACTIONS = [
        "follow_route"
    ]

    VALID_ROUTES = [
        "perimeter_loop",
        "inspection_loop",
        "warehouse_route"
    ]

    def validate(self, mission):

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

            if action["route"] not in self.VALID_ROUTES:
                print(f"[ERROR] Unsupported route: {action['route']}")
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