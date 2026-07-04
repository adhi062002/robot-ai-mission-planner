from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='robot_ai_mission_planner',
            executable='initial_pose_publisher',
            name='initial_pose_publisher',
            output='screen'
        ),
        Node(
            package='robot_ai_mission_planner',
            executable='mission_executor',
            name='mission_executor',
            output='screen'
        ),
    ])
