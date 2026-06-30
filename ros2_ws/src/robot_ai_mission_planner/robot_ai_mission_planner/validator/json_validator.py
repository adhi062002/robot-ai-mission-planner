from robot_ai_mission_planner.interfaces.mission_schema import MISSION_SCHEMA


class MissionValidator:

    def validate(self, mission):

        for key in MISSION_SCHEMA:

            if key not in mission:
                return False

            if not isinstance(mission[key], MISSION_SCHEMA[key]):
                return False

        if len(mission["actions"]) == 0:
            return False

        action = mission["actions"][0]

        required = [
            "type",
            "route",
            "laps",
            "speed"
        ]

        for key in required:

            if key not in action:
                return False

        return True
