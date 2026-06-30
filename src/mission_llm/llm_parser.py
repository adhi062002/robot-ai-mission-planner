class MissionLLM:

    def parse(self, prompt):

        prompt = prompt.lower()

        route = "inspection_loop"

        if "perimeter" in prompt:
            route = "perimeter_loop"

        elif "warehouse" in prompt:
            route = "warehouse_route"

        laps = 1

        if "twice" in prompt:
            laps = 2

        elif "thrice" in prompt:
            laps = 3

        speed = 0.3

        if "fast" in prompt:
            speed = 0.6

        elif "slow" in prompt:
            speed = 0.2

        return {

            "mission": "navigation",

            "actions": [

                {

                    "type": "follow_route",

                    "route": route,

                    "laps": laps,

                    "speed": speed

                }

            ]
        }
