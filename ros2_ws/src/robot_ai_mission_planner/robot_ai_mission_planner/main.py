from robot_ai_mission_planner.mission_llm.rule_based_planner import MissionLLM
from robot_ai_mission_planner.validator.json_validator import MissionValidator
from robot_ai_mission_planner.executor.mission_executor import MissionExecutor


def main():

    prompt = input("Mission > ")

    llm = MissionLLM()

    validator = MissionValidator()

    executor = MissionExecutor()

    mission = llm.parse(prompt)

    print("\nGenerated Mission JSON\n")
    print(mission)

    if validator.validate(mission):

        print("\nMission Validated Successfully")

        executor.execute(mission)

    else:

        print("\nMission Validation Failed")


if __name__ == "__main__":
    main()
