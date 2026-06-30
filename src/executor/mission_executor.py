import json


class MissionExecutor:

    def execute(self, mission):

        print("\n===== EXECUTING MISSION =====")

        action = mission["actions"][0]

        filename = f"missions/{action['route']}.json"

        with open(filename, "r") as f:

            route = json.load(f)

        print(f"Mission : {mission['mission']}")
        print(f"Route   : {route['name']}")
        print(f"Laps    : {action['laps']}")
        print(f"Speed   : {action['speed']}")

        print("\nWaypoints")

        for wp in route["waypoints"]:

            print(wp)

        print("\nMission Complete")
