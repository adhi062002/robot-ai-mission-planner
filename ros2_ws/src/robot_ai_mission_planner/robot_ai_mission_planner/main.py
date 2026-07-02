import time

import rclpy

from robot_ai_mission_planner.mission_llm.ollama_planner import MissionLLM
from robot_ai_mission_planner.validator.json_validator import MissionValidator
from robot_ai_mission_planner.mission_publisher import MissionPublisher


def main():

    rclpy.init()

    publisher = MissionPublisher()

    prompt = input("Mission > ")

    llm = MissionLLM()
    validator = MissionValidator()

    start = time.time()

    mission = llm.parse(prompt)

    inference_time = time.time() - start

    print(f"\nInference Time: {inference_time:.2f} seconds")

    if mission is None:

        print("\nMission generation failed.")

        publisher.destroy_node()
        rclpy.shutdown()

        return

    print("\nGenerated Mission JSON\n")
    print(mission)

    if not validator.validate(mission):

        print("\nMission Validation Failed. Mission was not published.")

        publisher.destroy_node()
        rclpy.shutdown()

        return

    print("\nMission Validated Successfully")

    publisher.publish_mission(mission)

    print("\nMission published successfully.")

    publisher.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()