
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dual_laser_merger',
            executable='dual_laser_merger_node',
            remappings=[
                ('laser_1','/scan'),
                ('laser_2','/image_scan'),
                ('merged', '/merged_image_scan')
            ],
            parameters=[{

            'publish_rate': 10,
            'target_frame': 'base_link',
            'angle_increment': 0.001,
            'scan_time': 0.033 ,
            'range_min': 0.01,
            'range_max': 25.0,
            'min_height': -1.0,
            'max_height': 1.0,
            'angle_min': -3.141592654,
            'angle_max': 3.141592654,
            'use_inf': False
              
            }]
        )
    ])



