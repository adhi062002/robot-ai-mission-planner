import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from robot_ai_mission_planner.executor.mission_executor import MissionExecutor


class MissionSubscriber(Node):

    def __init__(self):

        super().__init__("mission_subscriber")

        self.mission_executor = MissionExecutor(self)

        self.subscription = self.create_subscription(
            String,
            "/mission_command",
            self.callback,
            10
        )

        self.get_logger().info("Mission Subscriber Ready")

    def callback(self, msg):

        try:
            data = json.loads(msg.data)
        except json.JSONDecodeError:
            self.get_logger().error("Invalid JSON on /mission_command")
            return

        if isinstance(data, dict) and data.get("command") == "shutdown":

            self.get_logger().info("Shutdown command received.")

            print("\nShutdown command received.")
            print("Shutting down...\n")

            rclpy.shutdown()
            return

        self.get_logger().info("Mission Received")

        print("\nReceived Mission JSON\n")
        print(data)

        self.mission_executor.execute(data)