#!/usr/bin/env python3

import subprocess
import time
import signal
import sys
import threading

processes = []


def launch(command, name):

    print(f"\n========== Starting {name} ==========\n")

    process = subprocess.Popen(command)

    processes.append(process)

    return process


def wait_for_odom():

    print("Waiting for Gazebo...")

    while True:

        result = subprocess.run(
            [
                "ros2",
                "topic",
                "echo",
                "/odom",
                "--once"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print("✓ Gazebo Ready")
            return

        time.sleep(1)


def wait_for_nav2():

    print("Waiting for Navigation2...")

    while True:

        result = subprocess.run(
            [
                "ros2",
                "service",
                "call",
                "/lifecycle_manager_navigation/is_active",
                "std_srvs/srv/Trigger",
                "{}"
            ],
            capture_output=True,
            text=True
        )

        if "success: true" in result.stdout:
            print("✓ Navigation2 Ready")
            return

        time.sleep(2)


def shutdown(signum=None, frame=None):

    print("\n\nShutting down system...\n")

    for process in reversed(processes):

        if process.poll() is None:
            process.terminate()

    time.sleep(2)

    for process in reversed(processes):

        if process.poll() is None:
            process.kill()

    print("System shutdown complete.")

    sys.exit(0)

def launch_initial_pose():

    launch(
        [
            "ros2",
            "run",
            "robot_ai_mission_planner",
            "initial_pose_publisher"
        ],
        "Initial Pose Publisher"
    )

def main():

    signal.signal(signal.SIGINT, shutdown)

    # --------------------------------------------------
    # Gazebo
    # --------------------------------------------------

    launch(
        [
            "ros2",
            "launch",
            "turtlebot3_gazebo",
            "turtlebot3_world.launch.py"
        ],
        "Gazebo"
    )

    wait_for_odom()

    # --------------------------------------------------
    # Navigation2
    # --------------------------------------------------

    launch(
        [
            "ros2",
            "launch",
            "turtlebot3_navigation2",
            "navigation2.launch.py",
            "use_sim_time:=True"
        ],
        "Navigation2"
    )

    

    # # --------------------------------------------------
    # # Initial Pose Publisher
    # # --------------------------------------------------

    # pose_thread = threading.Thread(
    # target=launch_initial_pose,
    # daemon=True
    #  )

    # pose_thread.start()

    # wait_for_nav2()

    # # --------------------------------------------------
    # # Mission Executor
    # # --------------------------------------------------

    # launch(
    #     [
    #         "ros2",
    #         "run",
    #         "robot_ai_mission_planner",
    #         "mission_executor"
    #     ],
    #     "Mission Executor"
    # )

    print("\n======================================")
    print(" Robot AI Mission Planner Ready")
    print("======================================")
    print("You can now run:")
    print("ros2 run robot_ai_mission_planner initial_pose_publisher ")
    print("ros2 run robot_ai_mission_planner mission_planner")
    print("ros2 run robot_ai_mission_planner mission_executor")
    print("======================================\n")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()