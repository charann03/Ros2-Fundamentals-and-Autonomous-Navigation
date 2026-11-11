
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='dual_laser_merger',
            executable='dual_laser_merger_node',
            remappings=[
                ('laser_1','/scan'),
                ('laser_2','/cloud_scan'),
                ('merged', '/merged_cloud_scan')
            ],
            parameters=[{

            'publish_rate': 100,
            'target_frame': 'base_link',
            'angle_increment': 0.001,
            'scan_time': 0.3333 ,
            'range_min': 0.5,
            'range_max': 20.0,
            'min_height': 0.1,
            'max_height': 2.0,
            'angle_min': -3.141592654,
            'angle_max': 3.141592654,
            'use_inf': False
              
            }]
        )
    ])

# from ament_index_python.packages import get_package_share_directory
# from launch import LaunchDescription
# from launch.actions import IncludeLaunchDescription
# from launch.launch_description_sources import PythonLaunchDescriptionSource


# def generate_launch_description():

#     ld = LaunchDescription()

#     dual_laser_merger_node = IncludeLaunchDescription(
#         PythonLaunchDescriptionSource(
#             [
#                 f"{get_package_share_directory('dual_laser_merger')}/demo_laser_merger.launch.py"
#             ]
#         ),
#         launch_arguments={
#             'laser_1_topic': '/scan',
#             'laser_2_topic': '/cloud_scan',
#             'merged_topic': 'merged/scan',
#             'publish_rate': '100',
#             'target_frame': 'base_link',
#             'angle_increment': '0.001',
#             'scan_time': '0.067',
#             'range_min': '0.01',
#             'range_max': '25.0',
#             'min_height': '-1.0',
#             'max_height': '1.0',
#             'angle_min': '-3.141592654',
#             'angle_max': '3.141592654',
#             'use_inf': 'false',
#         }.items(),
#     )

#     ld.add_action(dual_laser_merger_node)

#     return ld



