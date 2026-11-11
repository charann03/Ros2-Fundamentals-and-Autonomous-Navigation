
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    param_config = os.path.join(
        get_package_share_directory('nav_custom_pkg'), 'config', 'depthimg2lsrscn.yaml')
    return LaunchDescription([
        Node(
            package='depthimage_to_laserscan',
            executable='depthimage_to_laserscan_node',
            name='depthimage_to_laserscan',
            remappings=[('depth', '/camera/depth/image_raw' ),
                        ('depth_camera_info', '/camera/depth/camera_info'),
                        ('scan' , '/image_scan')],
            parameters=[param_config])
    ])