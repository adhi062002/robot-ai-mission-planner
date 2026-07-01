import json
import os

import rclpy
from rclpy.action import ActionClient
from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose

from ament_index_python.packages import get_package_share_directory


class MissionExecutor:

    def __init__(self, node):
        self.node = node

        # Nav2 action client
        self.nav_client = ActionClient(
            node,
            NavigateToPose,
            "navigate_to_pose"
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

        # Wait for Nav2 action server
        if not self.nav_client.wait_for_server(timeout_sec=5.0):
            print("[ERROR] Nav2 action server not available")
            return False

        goal_msg = NavigateToPose.Goal()

        pose = PoseStamped()
        pose.header.frame_id = "map"
        pose.header.stamp = self.node.get_clock().now().to_msg()

        pose.pose.position.x = float(x)
        pose.pose.position.y = float(y)
        pose.pose.position.z = 0.0

        # No orientation control (simple navigation)
        pose.pose.orientation.w = 1.0

        goal_msg.pose = pose

        # Send goal
        send_goal_future = self.nav_client.send_goal_async(goal_msg)

        rclpy.spin_until_future_complete(self.node, send_goal_future)

        goal_handle = send_goal_future.result()

        if not goal_handle.accepted:
            print("[ERROR] Goal rejected by Nav2")
            return False

        # Wait for result
        result_future = goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self.node, result_future)

        result = result_future.result()

        return result.status == 4  # STATUS_SUCCEEDED

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