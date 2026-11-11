import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription , TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration , Command
from launch.actions import DeclareLaunchArgument , RegisterEventHandler
from launch_ros.actions import Node
from launch.event_handlers import OnProcessExit



def generate_launch_description():
    
    package_name= 'clean_bot'
    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time_cmd = DeclareLaunchArgument(
    'use_sim_time',
    default_value='true',
    description='Use simulation (Gazebo) clock if true')


    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('multi_robot_description'))
    # pkg_path = os.path.join(get_package_share_directory('clean_bot'))

    xacro_file = os.path.join(pkg_path,'dummy','clean_bot.xacro')

    # xacro_file = os.path.join(pkg_path,'urdf','clean_bot.xacro')
    # xacro_file = '/home/charann-inc5751/custom_multi_rbt_ws/src/multi_robot_description/dummy/clean_bot.xacro'

    gazebo_params_file = os.path.join(
                    get_package_share_directory(package_name),'params','gazebo_params.yaml'
                )
    # gazebo_world_file = os.path.join(
    #                 get_package_share_directory(package_name),'world',"wall_4x4_edt.world"
    #             )
    gazebo_world_file = os.path.join(
                    get_package_share_directory(package_name),'world',"test2.world"
                )
    # gazebo_world_file = os.path.join(
    #                 get_package_share_directory("nav_custom_pkg"),'worlds','maze_scale.world'
    #             )
    #map the use_ros2_contol_ value to use ros2_contol plugins(default=true#refer_tortoisebot_depth_cam_lidar.xacro) and gazebo diff drive plugins .toxml() converts the zacro as a string
    # robot_description_config = xacro.process_file(xacro_file, mappings={"use_ros2_control" : "true"}).toxml()

    #to change the use_ros2_control from our main launch file tortoisebot_ros2_control.launch.py 
    robot_description_config = Command(["xacro ", xacro_file])

    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config, 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    #jsp
    joint_state_publisher_node = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': robot_description_config}],
        )
    
    #gazebo
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={
                                      'world': gazebo_world_file}.items()
             )


    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_clean_bot',
                                            #    '-x', '-1.5', '-y', '1.5', '-z', '0.10',
                                            #    '-R', '0.0', '-P', '0.0', '-Y', '0.0'
                                               ],
                        output='screen')
    
        # Delayed spawners
    # delayed_clean_bot_spawner = RegisterEventHandler(
    #     event_handler=OnProcessExit(
    #         target_action=gazebo,
    #         on_exit=[spawn_entity]
    #     )
    # )

    delayed_spawn = TimerAction(
        period=2.0,
        actions=[spawn_entity]
    )


    return LaunchDescription([
        declare_use_sim_time_cmd,
        # joint_state_publisher_node,
        node_robot_state_publisher,
        gazebo,
        # delayed_clean_bot_spawner
        delayed_spawn

    ])
