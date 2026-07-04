import time

import rclpy

from robot_ai_mission_planner.mission_llm.ollama_planner import MissionLLM
from robot_ai_mission_planner.validator.json_validator import MissionValidator
from robot_ai_mission_planner.mission_publisher import MissionPublisher


def main():

    rclpy.init()

    publisher = MissionPublisher()
    llm = MissionLLM()
    validator = MissionValidator()

    print("\n==========================================")
    print(" Robot AI Mission Planner")
    print("==========================================")
    print("Type a mission prompt, or 'quit' to exit.\n")

    try:
        while True:

            prompt = input("Mission > ").strip()

            if prompt == "":
                continue

            if prompt.lower() in ("quit", "exit"):

                print("\nSending shutdown command...")

                publisher.publish_shutdown()

                # Give the message a moment to actually go out over DDS
                # before we tear the publisher node down.
                time.sleep(0.5)

                break

            start = time.time()

            mission = llm.parse(prompt)

            inference_time = time.time() - start

            print(f"\nInference Time: {inference_time:.2f} seconds")

            if mission is None:
                print("\nMission generation failed.\n")
                continue

            print("\nGenerated Mission JSON\n")
            print(mission)

            if not validator.validate(mission):
                print("\nMission Validation Failed. Mission was not published.\n")
                continue

            print("\nMission Validated Successfully")

            publisher.publish_mission(mission)

            print("\nMission published successfully.\n")

    finally:
        publisher.destroy_node()
        rclpy.shutdown()
        print("\nMission Planner exited.\n")


if __name__ == "__main__":
    main()