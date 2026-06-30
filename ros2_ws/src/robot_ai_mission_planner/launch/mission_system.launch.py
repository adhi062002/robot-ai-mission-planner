import os

from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    package_dir = get_package_share_directory("robot_ai_mission_planner")

    publisher_node = Node(
        package="robot_ai_mission_planner",
        executable="mission_publisher",
        name="mission_publisher",
        output="screen",
        emulate_tty=True
    )

    executor_node = Node(
        package="robot_ai_mission_planner",
        executable="mission_executor_node",
        name="mission_executor_node",
        output="screen",
        emulate_tty=True
    )

    return LaunchDescription([
        publisher_node,
        executor_node
    ])