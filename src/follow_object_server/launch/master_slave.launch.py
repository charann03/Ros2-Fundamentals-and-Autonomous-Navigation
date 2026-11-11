from launch import LaunchDescription
import launch
import launch_ros.actions
from launch.actions import DeclareLaunchArgument, ExecuteProcess, IncludeLaunchDescription , TimerAction, OpaqueFunction
from launch.conditions import IfCondition, UnlessCondition, LaunchConfigurationNotEquals, LaunchConfigurationEquals
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression, TextSubstitution

from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, EmitEvent, RegisterEventHandler
from launch.event_handlers import OnProcessExit
import os
from ament_index_python.packages import get_package_share_directory
import xacro
import sys
# sys.path.append("custom_multi_rbt_ws/src/multi_robot_gazebo/launch") 
# from tb3_multi_slam.robot_list import *
# from nav2_common.launch import RewrittenYaml
import tempfile

robots = [
    {'name': '', 'x_pos': 0.0, 'y_pos': 0.0, 'z_pos': 0.1,
        "robot_material_name" : 'Blue', "robot_color" : "blue"},
    {'name': 'master', 'x_pos': 1.0, 'y_pos': 0.0, 'z_pos': 0.1,
        "robot_material_name" : 'Green', "robot_color" : "green"},
]

def generate_launch_description():
    # urdf_pkg_path = os.path.join(get_package_share_directory('turtlebot3_description'))
    urdf_file = os.path.join(get_package_share_directory("follow_object_server"),
                              'urdf', 'turtlebot3_waffle.urdf')
    gazebo_world_file_pkg = 'clean_bot_docking'
    ld = []
    last_action = None

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    #Launch gazebo FIRST
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(gazebo_world_file_pkg), 'launch', 'cafe.launch.py')]),
                    launch_arguments={
                                    #   'world': gazebo_world_file,
                                      'gui': 'true'
                                      }.items()
             )

    for robot in robots:
        namespace =  robot['name'] if robot['name'] != "" else ""

        robot_description_config = xacro.process_file(
            urdf_file,
            mappings={
                "namespace": robot['name']
            },
        )

        params = {
            'robot_description': robot_description_config.toxml(),
            'use_sim_time': use_sim_time
        }

        start_robot_state_publisher_cmd = Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            # name='robot_state_publisher',
            namespace= namespace,
            output='screen',
            # remappings=remappings,
            parameters=[params]
        )

        spawn_entity_cmd = Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            namespace= namespace,
            arguments=[
                "-topic", "robot_description",
                '-entity', robot['name'],
                '-x', str(robot['x_pos']),
                '-y', str(robot['y_pos']),
                '-z', str(robot['z_pos']),
                '-Y', '0.0',
                '-R', '0.0',
                '-P', '0.0',
            ],
            parameters=[{'use_sim_time': use_sim_time}],
            output='screen')
        

        
        if last_action is None:
            ld.extend([
                start_robot_state_publisher_cmd,
                spawn_entity_cmd,

            ])
        else:
            spawn_robot_event = RegisterEventHandler(
                event_handler=OnProcessExit(
                    target_action=last_action,
                    on_exit=[
                        spawn_entity_cmd,
                        start_robot_state_publisher_cmd,
                    ],
                )
            )

            ld.append(spawn_robot_event)

        last_action = spawn_entity_cmd
    launch_des = LaunchDescription()
    launch_des.add_action(gazebo)
    for node in ld:
        launch_des.add_action(node)
    return launch_des

        

        
