from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    talker_node = Node(
        package="my_robot_py_pkg",
        executable="robot_news",
    )

    listener_node = Node(
        package="my_robot_py_pkg",
        executable="smartPhone_sub"
    )

    ld.add_action(talker_node)
    ld.add_action(listener_node)

    return ld