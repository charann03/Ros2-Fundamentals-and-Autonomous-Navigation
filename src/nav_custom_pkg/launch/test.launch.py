from launch import LaunchDescription
from launch_ros.actions import Node, SetParameter
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition
import os


def generate_launch_description():

    parameters = {
        'frame_id': 'base_link',
        'odom_frame_id': 'odom',

        # Subscriptions
        'subscribe_depth': True,
        'subscribe_scan': True,
        'subscribe_rgb': False,
        'approx_sync': True,

        # Registration strategy (ICP for LIDAR fusion)
        'Reg/Strategy': '1',        # ICP
        'Reg/Force3DoF': 'true',    # 2D motion

        # Mapping settings
        'Grid/FromDepth': 'true',
        'Grid/RangeMax': '8',

        # Performance tuning
        'Mem/STMSize': '30',
        'Icp/VoxelSize': '0.05',
    }

    remappings = [
        ('depth/image', '/camera/depth/image_raw'),
        ('depth/camera_info', '/camera/depth/camera_info'),
        ('scan', '/scan'),
        ('odom', '/odom')
    ]

    return LaunchDescription([

        # Use Gazebo simulation time
        SetParameter(name='use_sim_time', value=True),

        # RTAB-Map SLAM node
        Node(
            package='rtabmap_slam',
            executable='rtabmap',
            name='rtabmap',
            output='screen',
            parameters=[parameters],
            remappings=remappings,
            arguments=['-d']  # Deletes previous map database
        ),

        # RTAB-Map visualization tool
        Node(
            package='rtabmap_viz',
            executable='rtabmap_viz',
            name='rtabmap_viz',
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),

        # Optional RViz
        # Node(
        #     package='rviz2',
        #     executable='rviz2',
        #     name='rviz2',
        #     output='screen',
        #     condition=IfCondition(LaunchConfiguration("rviz")),
        # ),
    ])