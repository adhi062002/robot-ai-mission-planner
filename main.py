from src.mission_llm.llm_parser import MissionLLM
from src.validator.json_validator import MissionValidator
from src.executor.mission_executor import MissionExecutor


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
