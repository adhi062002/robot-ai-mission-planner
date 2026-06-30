import json

import rclpy
from rclpy.node import Node

from std_msgs.msg import String


class ROS2Interface(Node):

    def __init__(self):

        rclpy.init(args=None)

        super().__init__("mission_interface")

        self.publisher = self.create_publisher(
            String,
            "/mission_command",
            10
        )

        self.get_logger().info("ROS2 Interface Ready")

    def follow_route(self, route, laps, speed):

        mission = {

            "route": route["name"],
            "laps": laps,
            "speed": speed

        }

        msg = String()

        msg.data = json.dumps(mission)

        self.publisher.publish(msg)

        self.get_logger().info(f"Published: {msg.data}")

        rclpy.spin_once(self, timeout_sec=0.1)

    def shutdown(self):

        self.destroy_node()

        rclpy.shutdown()