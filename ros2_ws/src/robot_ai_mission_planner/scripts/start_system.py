#!/usr/bin/env python3

import subprocess
import time
import signal
import sys
import threading
import os

processes = []
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


def launch(command, name):

    print(f"\n========== Starting {name} ==========\n", flush=True)

    log_path = os.path.join(LOG_DIR, f"{name.lower().replace(' ', '_')}.log")
    log_file = open(log_path, "w")

    process = subprocess.Popen(
        command,
        stdout=log_file,
        stderr=subprocess.STDOUT
    )

    processes.append((process, log_file))

    print(f"  -> logging to {log_path}", flush=True)

    return process


def wait_for_odom():

    print("Waiting for Gazebo...", flush=True)

    while True:

        result = subprocess.run(
            ["ros2", "topic", "echo", "/odom", "--once"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        if result.returncode == 0:
            print("✓ Gazebo Ready", flush=True)
            return

        time.sleep(1)


def wait_for_nav2():

    print("Waiting for Navigation2...", flush=True)

    while True:

        result = subprocess.run(
            [
                "ros2", "service", "call",
                "/lifecycle_manager_navigation/is_active",
                "std_srvs/srv/Trigger", "{}"
            ],
            capture_output=True,
            text=True
        )

        if "success: true" in result.stdout:
            print("✓ Navigation2 Ready", flush=True)
            return

        time.sleep(2)


def shutdown(signum=None, frame=None):

    print("\n\nShutting down system...\n", flush=True)

    for process, log_file in reversed(processes):
        if process.poll() is None:
            process.terminate()

    time.sleep(2)

    for process, log_file in reversed(processes):
        if process.poll() is None:
            process.kill()
        log_file.close()

    print("System shutdown complete.", flush=True)

    sys.exit(0)


def launch_initial_pose():

    launch(
        ["ros2", "run", "robot_ai_mission_planner", "initial_pose_publisher"],
        "Initial Pose Publisher"
    )


def main():

    signal.signal(signal.SIGINT, shutdown)

    # --------------------------------------------------
    # Gazebo
    # --------------------------------------------------

    launch(
        ["ros2", "launch", "turtlebot3_gazebo", "turtlebot3_world.launch.py"],
        "Gazebo"
    )

    wait_for_odom()

    # --------------------------------------------------
    # Navigation2
    # --------------------------------------------------

    launch(
        ["ros2", "launch", "turtlebot3_navigation2", "navigation2.launch.py", "use_sim_time:=True"],
        "Navigation2"
    )

    # --------------------------------------------------
    # Initial Pose Publisher
    # --------------------------------------------------

    pose_thread = threading.Thread(
        target=launch_initial_pose,
        daemon=True
    )
    pose_thread.start()

    wait_for_nav2()

    # --------------------------------------------------
    # Mission Executor
    # --------------------------------------------------

    launch(
        ["ros2", "run", "robot_ai_mission_planner", "mission_executor"],
        "Mission Executor"
    )

    print("\n======================================", flush=True)
    print(" Robot AI Mission Planner Ready", flush=True)
    print("======================================", flush=True)
    print("You can now run:", flush=True)
    print("ros2 run robot_ai_mission_planner mission_planner", flush=True)
    print("======================================\n", flush=True)

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
