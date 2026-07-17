import os
import sys
import json
import tty
import termios
import threading
import signal
import time

import rclpy
from rclpy.node import Node
from rclpy.time import Time

from geometry_msgs.msg import Twist

import tf2_ros
from tf2_ros import TransformException

from ament_index_python.packages import get_package_share_directory


class RouteRecorder(Node):

    def __init__(self):
        super().__init__("route_recorder")

        self.package_share = get_package_share_directory(
            "robot_ai_mission_planner"
        )
        self.mission_dir = os.path.join(self.package_share, "missions")
        os.makedirs(self.mission_dir, exist_ok=True)

        self.mission_name = None
        self.filename = None

        self.cmd_pub = self.create_publisher(Twist, "/cmd_vel", 10)

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        self.linear_speed = 0.2
        self.angular_speed = 0.8

        self.waypoints = []

        # Track terminal state so we can always restore it, even mid-interrupt
        self._term_fd = sys.stdin.fileno()
        self._old_term_settings = None

    # ---------- Pose ----------

    def get_current_pose(self):
        try:
            t = self.tf_buffer.lookup_transform(
                "map",
                "base_footprint",
                Time()
            )
            x = t.transform.translation.x
            y = t.transform.translation.y
            return x, y

        except TransformException as ex:
            self.get_logger().warn(f"TF lookup failed: {ex}")
            return None, None

    def wait_for_tf(self):
        print("\nWaiting for TF...")

        while rclpy.ok():
            x, y = self.get_current_pose()

            if x is not None:
                print("TF Ready.\n")
                return

            time.sleep(0.2)

    # ---------- Mission naming ----------

    def get_mission_name(self):
        while True:
            print("\n==========================================")
            print(" Robot AI Mission Route Recorder")
            print("==========================================")

            mission_name = input("\nMission Name > ").strip()

            if mission_name == "":
                print("\nMission name cannot be empty.\n")
                continue

            filename = os.path.join(self.mission_dir, f"{mission_name}.json")

            if os.path.exists(filename):
                choice = input(
                    "\nMission already exists.\nOverwrite? (y/n): "
                ).lower()

                if choice == "y":
                    self.mission_name = mission_name
                    self.filename = filename
                    return
                elif choice == "n":
                    print("\nEnter another mission name.\n")
                    continue
                else:
                    print("\nInvalid choice.\n")
                    continue
            else:
                self.mission_name = mission_name
                self.filename = filename
                return

    # ---------- Keyboard ----------

    def get_key(self):
        old_settings = termios.tcgetattr(self._term_fd)
        self._old_term_settings = old_settings

        try:
            tty.setraw(self._term_fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(self._term_fd, termios.TCSADRAIN, old_settings)
            self._old_term_settings = None

        return key

    def restore_terminal(self):
        """Force-restore terminal settings if we get interrupted mid-read."""
        if self._old_term_settings is not None:
            termios.tcsetattr(
                self._term_fd, termios.TCSADRAIN, self._old_term_settings
            )
            self._old_term_settings = None

    def publish_twist(self, linear, angular):
        msg = Twist()
        msg.linear.x = linear
        msg.angular.z = angular
        self.cmd_pub.publish(msg)

    # ---------- JSON output ----------

    def save_mission(self):
        if not self.filename or not self.mission_name:
            print("\nNo mission name set.\n")
            return

        if len(self.waypoints) == 0:
            print("\nNo waypoints recorded. Mission not saved.\n")
            return

        data = {
            "name": self.mission_name,
            "waypoints": self.waypoints
        }

        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4
            )

        # Verify file contents
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                verify = json.load(f)

            if (
                verify["name"] == self.mission_name
                and len(verify["waypoints"]) == len(self.waypoints)
            ):
                print("\nMission verified successfully.")
            else:
                print("\nWARNING: Verification failed.")

        except Exception as e:
            print(f"\nVerification Error: {e}")

        print(f"\nMission saved to:\n{self.filename}")

    def handle_sigint(self, signum, frame):
        """Ctrl+C handler: stop the robot, restore terminal, save partial progress."""
        self.publish_twist(0.0, 0.0)
        self.restore_terminal()

        print("\n\nInterrupted (Ctrl+C)")
        print("Recorded Waypoints So Far\n")

        for i, waypoint in enumerate(self.waypoints, start=1):
            print(f"{i}: {waypoint}")

        if len(self.waypoints) > 0:
            print("\nSaving partial route...")
            self.save_mission()
        else:
            print("\nNo waypoints recorded.")

        self.destroy_node()
        rclpy.shutdown()
        sys.exit(0)

    # ---------- Teleop ----------

    def teleop(self):
        print("\n==========================================")
        print(" Teleoperation Started")
        print("==========================================\n")
        print("Controls")
        print("------------------------------------------")
        print("W : Forward")
        print("S : Backward")
        print("A : Turn Left")
        print("D : Turn Right")
        print("SPACE : Stop Robot")
        print("V : Save Waypoint")
        print("Q : Finish Recording")
        print("Ctrl+C : Abort & Save Partial Route")
        print("------------------------------------------")

        while True:
            key = self.get_key().lower()

            if key == "w":
                self.publish_twist(self.linear_speed, 0.0)
                print("Forward")

            elif key == "s":
                self.publish_twist(-self.linear_speed, 0.0)
                print("Backward")

            elif key == "a":
                self.publish_twist(0.0, self.angular_speed)
                print("Turning Left")

            elif key == "d":
                self.publish_twist(0.0, -self.angular_speed)
                print("Turning Right")

            elif key == " ":
                self.publish_twist(0.0, 0.0)
                print("Robot Stopped")

            elif key == "v":
                x, y = self.get_current_pose()

                if x is None:
                    print("\nCould not get pose from TF, try again.\n")
                    continue

                waypoint = [round(x, 3), round(y, 3)]

                if len(self.waypoints) > 0 and waypoint == self.waypoints[-1]:
                    print("\nDuplicate waypoint ignored.\n")
                    continue

                self.waypoints.append(waypoint)
                print(f"\nWaypoint {len(self.waypoints)} Saved")
                print(f"x = {waypoint[0]}, y = {waypoint[1]}")

            elif key == "q":
                self.publish_twist(0.0, 0.0)
                print("\nRecording Finished")
                print("\nRecorded Waypoints\n")

                for i, waypoint in enumerate(self.waypoints, start=1):
                    print(f"{i}: {waypoint}")

                self.save_mission()
                break

    def run(self):
        self.get_mission_name()
        print(f"\nMission : {self.mission_name}")
        self.wait_for_tf()
        self.teleop()


def main():
    rclpy.init()
    recorder = RouteRecorder()

    # Register SIGINT handler after node is constructed so cmd_pub etc. exist
    signal.signal(signal.SIGINT, recorder.handle_sigint)

    spin_thread = threading.Thread(
        target=rclpy.spin, args=(recorder,), daemon=True
    )
    spin_thread.start()

    try:
        recorder.run()
    finally:
        recorder.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()