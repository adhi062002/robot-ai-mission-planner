import rclpy

from robot_ai_mission_planner.mission_llm.rule_based_planner import MissionLLM
from robot_ai_mission_planner.validator.json_validator import MissionValidator
from robot_ai_mission_planner.mission_publisher import MissionPublisher


def main():

    rclpy.init()

    publisher = MissionPublisher()

    prompt = input("Mission > ")

    llm = MissionLLM()

    validator = MissionValidator()

    mission = llm.parse(prompt)

    print("\nGenerated Mission JSON\n")
    print(mission)

    if validator.validate(mission):

        print("\nMission Validated Successfully")

        publisher.publish_mission(mission)

    else:

        print("\nMission Validation Failed")

    publisher.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()