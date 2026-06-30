import rclpy

from robot_ai_mission_planner.mission_subscriber import MissionSubscriber


def main(args=None):

    rclpy.init(args=args)

    node = MissionSubscriber()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()