import json

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MissionPublisher(Node):

    def __init__(self):

        super().__init__("mission_publisher")

        self.publisher = self.create_publisher(
            String,
            "/mission_command",
            10
        )

    def publish_mission(self, mission):

        msg = String()

        msg.data = json.dumps(mission)

        self.publisher.publish(msg)

        self.get_logger().info(
            "Mission Published"
        )