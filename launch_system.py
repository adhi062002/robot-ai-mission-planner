#!/usr/bin/env python3

import os
import signal
import subprocess
import sys
import time


processes = []


# Inside the container, the workspace lives at /root/ros2_ws
WORKSPACE = os.environ.get("ROS_WS", "/root/ros2_ws")

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


def wait_for_ollama():

    print("Waiting for Ollama...")

    while True:

        result = subprocess.run(
            [
                "bash",
                "-c",
                "curl -s http://localhost:11434/api/tags > /dev/null"
            ]
        )

        if result.returncode == 0:
            print("✓ Ollama Ready")
            return

        time.sleep(1)


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

        # NOTE: ros2 service call prints Python-style booleans
        # ("success: True", capital T) -- not "true". Checking
        # case-insensitively avoids this getting stuck forever.
        if result.returncode == 0 and "true" in result.stdout.lower():
            print("✓ Navigation2 Ready")
            return

        time.sleep(2)


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
            return

        time.sleep(1)


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
    signal.signal(signal.SIGTERM, shutdown)

    # --------------------------------------------------
    # Ollama (mission planner/executor depend on it)
    # --------------------------------------------------

    wait_for_ollama()

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

    wait_for_nav2()
    wait_for_initialpose_subscriber()

    # --------------------------------------------------
    # Initial Pose Publisher + Mission Executor
    # (bundled into a single launch file)
    # --------------------------------------------------

    launch(
        [
            "ros2",
            "launch",
            "robot_ai_mission_planner",
            "post_nav2.launch.py"
        ],
        "Initial Pose + Mission Executor"
    )

    print("\n======================================")
    print(" Robot AI Mission Planner Ready")
    print("======================================")
    print("Open a second terminal into this container and run:")
    print("  docker exec -it <container_name> bash")
    print("  ros2 run robot_ai_mission_planner mission_planner")
    print("======================================\n")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
