import rclpy
from rclpy.executors import MultiThreadedExecutor, ExternalShutdownException

from robot_ai_mission_planner.mission_subscriber import MissionSubscriber


def main(args=None):

    rclpy.init(args=args)

    node = MissionSubscriber()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    except (KeyboardInterrupt, ExternalShutdownException):
       
        pass
    finally:
        executor.shutdown()
        node.destroy_node()

   
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()