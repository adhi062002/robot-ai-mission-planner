import json

from rclpy.node import Node
from std_msgs.msg import String

from robot_ai_mission_planner.executor.mission_executor import MissionExecutor


class MissionSubscriber(Node):

    def __init__(self):

        super().__init__("mission_subscriber")

        self.mission_executor = MissionExecutor()

        self.subscription = self.create_subscription(
            String,
            "/mission_command",
            self.callback,
            10
        )

        self.get_logger().info("Mission Subscriber Ready")

    def callback(self, msg):

        self.get_logger().info("Mission Received")

        mission = json.loads(msg.data)

        print("\nReceived Mission JSON\n")
        print(mission)

        self.mission_executor.execute(mission)