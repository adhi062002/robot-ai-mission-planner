import json
import os
import threading

import rclpy
from rclpy.action import ActionClient
from rclpy.callback_groups import ReentrantCallbackGroup
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

from ament_index_python.packages import get_package_share_directory


class MissionExecutor:

    def __init__(self, node):
        self.node = node

        self.nav_callback_group = ReentrantCallbackGroup()

        # Nav2 action client
        self.nav_client = ActionClient(
            node,
            NavigateToPose,
            "navigate_to_pose",
            callback_group=self.nav_callback_group
        )

    def execute(self, mission):

        print("\n========== Mission Executor ==========")

        for action in mission["actions"]:

            if action["type"] == "follow_route":

                route = self.load_route(action["route"])

                if route is None:
                    continue

                print("--------------------------------------")
                print(f"Route : {route['name']}")
                print(f"Laps  : {action['laps']}")
                print(f"Speed : {action['speed']}")
                print("--------------------------------------")

                print("\nWaypoints\n")

                for lap in range(action["laps"]):

                    print(f"\n--- Lap {lap + 1} ---\n")

                    for index, waypoint in enumerate(route["waypoints"], start=1):

                        x, y = waypoint

                        print(
                            f"Navigating to Waypoint {index}: x={x}, y={y}"
                        )

                        success = self.send_goal(x, y)

                        if success:
                            print("Goal reached\n")
                        else:
                            print("Goal failed\n")

            else:
                print(f"\n[WARNING] Unknown action: {action['type']}")

        print("\nMission Complete")

    def send_goal(self, x, y, yaw=0.0):

        print(f"\nSending goal to ({x}, {y})")

        if not self.nav_client.wait_for_server(timeout_sec=5.0):
            print("[ERROR] Nav2 action server not available")
            return False

        print("Nav2 server available")

        goal_msg = NavigateToPose.Goal()

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.node.get_clock().now().to_msg()

        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = 0.0

        pose.pose.orientation.x = 0.0
        pose.pose.orientation.y = 0.0
        pose.pose.orientation.z = 0.0
        pose.pose.orientation.w = 1.0

        goal_msg.pose = pose

        print("Sending action goal...")

        goal_response_event = threading.Event()
        goal_response_box = {}

        def on_goal_response(future):
            goal_response_box["handle"] = future.result()
            goal_response_event.set()

        send_goal_future = self.nav_client.send_goal_async(goal_msg)
        send_goal_future.add_done_callback(on_goal_response)

        if not goal_response_event.wait(timeout=10.0):
            print("[ERROR] Timed out waiting for goal to be accepted")
            return False

        goal_handle = goal_response_box.get("handle")

        if goal_handle is None:
            print("[ERROR] Goal handle is None")
            return False

        print("Goal accepted:", goal_handle.accepted)

        if not goal_handle.accepted:
            print("[ERROR] Goal rejected")
            return False

        print("Waiting for navigation result...")

        result_event = threading.Event()
        result_box = {}

        def on_result(future):
            result_box["result"] = future.result()
            result_event.set()

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(on_result)

        print("Result future created")

        if not result_event.wait(timeout=120.0):
            print("[ERROR] Timed out waiting for navigation result")
            return False

        result = result_box.get("result")

        print(result)

        print("Navigation status:", result.status)

        return result.status == 4
    def load_route(self, route_name):

        package_share = get_package_share_directory(
            "robot_ai_mission_planner"
        )

        filename = os.path.join(
            package_share,
            "missions",
            f"{route_name}.json"
        )

        try:
            with open(filename) as f:
                return json.load(f)

        except FileNotFoundError:
            print(f"\n[ERROR] Route file not found: {filename}")
            return None

        except json.JSONDecodeError:
            print(f"\n[ERROR] Invalid JSON in: {filename}")
            return None