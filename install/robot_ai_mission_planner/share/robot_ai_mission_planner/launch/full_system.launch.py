#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import threading
import time


processes = []


WORKSPACE = os.path.expanduser(
    "~/robot-ai-mission-planner/ros2_ws"
)

ROS_SETUP = (
    f"source /opt/ros/humble/setup.bash && "
    f"source {WORKSPACE}/install/setup.bash && "
)


def launch(command, name):

    print(f"\n========== Starting {name} ==========\n")

    cmd = ROS_SETUP + " ".join(command)

    process = subprocess.Popen(
        ["bash", "-c", cmd]
    )

    processes.append(process)

    return process


def wait_for_odom():

    print("Waiting for Gazebo...")

    while True:

        result = subprocess.run(
            [
                "bash",
                "-c",
                ROS_SETUP +
                "ros2 topic echo /odom --once"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:

            print("✓ Gazebo Ready")
            return

        time.sleep(1)


def wait_for_initialpose_subscriber():

    print("Waiting for AMCL to subscribe to /initialpose...")

    while True:

        result = subprocess.run(
            [
                "bash",
                "-c",
                ROS_SETUP +
                "ros2 topic info /initialpose"
            ],
            capture_output=True,
            text=True
        )

        if "Subscription count: 1" in result.stdout:

            print("✓ AMCL subscribed to /initialpose")

            launch(
                [
                    "ros2",
                    "run",
                    "robot_ai_mission_planner",
                    "initial_pose_publisher"
                ],
                "Initial Pose Publisher"
            )

            return

        time.sleep(1)


def wait_for_nav2():

    print("Waiting for Navigation2...")

    while True:

        result = subprocess.run(
            [
                "bash",
                "-c",
                ROS_SETUP +
                "ros2 service call "
                "/lifecycle_manager_navigation/is_active "
                "std_srvs/srv/Trigger '{}'"
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

    # --------------------------------------------------
    # Background thread waits until AMCL is actually
    # listening on /initialpose, then publishes once.
    # --------------------------------------------------

    pose_thread = threading.Thread(
        target=wait_for_initialpose_subscriber,
        daemon=True
    )

    pose_thread.start()

    # --------------------------------------------------
    # Wait until Nav2 is fully active
    # --------------------------------------------------

    wait_for_nav2()

    # --------------------------------------------------
    # Mission Executor
    # --------------------------------------------------

    launch(
        [
            "ros2",
            "run",
            "robot_ai_mission_planner",
            "mission_executor"
        ],
        "Mission Executor"
    )

    print("\n======================================")
    print(" Robot AI Mission Planner Ready")
    print("======================================")
    print("You can now run:")
    print("ros2 run robot_ai_mission_planner mission_planner")
    print("======================================\n")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()