import rclpy

from rclpy.node import Node

from std_msgs.msg import String


class MissionListener(Node):

    def __init__(self):

        super().__init__("mission_listener")

        self.subscription = self.create_subscription(
            String,
            "/mission_command",
            self.callback,
            10
        )

        self.get_logger().info("Waiting for missions...")

    def callback(self, msg):

        self.get_logger().info(f"Received: {msg.data}")


def main():

    rclpy.init()

    node = MissionListener()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":

    main()