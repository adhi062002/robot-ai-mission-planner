import os

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    gazebo_pkg = get_package_share_directory("turtlebot3_gazebo")
    nav2_bringup_pkg = get_package_share_directory("nav2_bringup")
    turtlebot3_nav2_pkg = get_package_share_directory("turtlebot3_navigation2")

    # ------------------------------------------------------------------
    # EDIT THIS: point to your actual map.yaml.
    # If you're reusing the stock turtlebot3 demo map, this default is
    # already correct — turtlebot3_nav2_pkg/map/map.yaml. If you built
    # your own map via SLAM, replace this with that path instead.
    # ------------------------------------------------------------------
    map_yaml_path = os.path.join(
        turtlebot3_nav2_pkg,
        "map",
        "map.yaml"
    )

    # nav2 params file, also bundled in turtlebot3_navigation2 — this is
    # what navigation2.launch.py was building internally via
    # TURTLEBOT3_MODEL + '.yaml'; we build it explicitly instead so
    # nothing depends on an env-var substitution resolving correctly
    # inside a nested include.
    turtlebot3_model = os.environ.get("TURTLEBOT3_MODEL", "burger")

    params_file_path = os.path.join(
        turtlebot3_nav2_pkg,
        "param",
        f"{turtlebot3_model}.yaml"
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                gazebo_pkg,
                "launch",
                "turtlebot3_world.launch.py"
            )
        )
    )

    # Calling nav2_bringup's bringup_launch.py directly instead of nesting
    # through turtlebot3_navigation2's navigation2.launch.py — that wrapper
    # builds its map/params paths from substitutions that can silently
    # resolve to an empty string ('') if anything upstream isn't set
    # exactly as it expects, which is what "No such file or directory: ''"
    # means. Passing explicit, known-good paths here avoids that class of
    # failure entirely.
    nav2 = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                nav2_bringup_pkg,
                "launch",
                "bringup_launch.py"
            )
        ),
        launch_arguments={
            "map": map_yaml_path,
            "params_file": params_file_path,
            "use_sim_time": "True",
            "autostart": "True"
        }.items()
    )

    initial_pose = Node(
        package="robot_ai_mission_planner",
        executable="initial_pose_publisher",
        output="screen"
    )

    mission_executor = Node(
        package="robot_ai_mission_planner",
        executable="mission_executor",
        output="screen"
    )

    delayed_nav2 = TimerAction(
        period=10.0,
        actions=[nav2]
    )

    delayed_initial_pose = TimerAction(
        period=15.0,
        actions=[initial_pose]
    )

    delayed_executor = TimerAction(
        period=17.0,
        actions=[mission_executor]
    )

    return LaunchDescription([
        gazebo,
        delayed_nav2,
        delayed_initial_pose,
        delayed_executor
    ])