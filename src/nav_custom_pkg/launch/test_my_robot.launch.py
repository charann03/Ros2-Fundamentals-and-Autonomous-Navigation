import os
from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch_ros.actions import Node



def generate_launch_description():
    

    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!

    package_name= 'nav_custom_pkg' #<--- CHANGE to your CURRENT package name ME

    use_ros2_control = LaunchConfiguration('use_ros2_control')
    declare_use_ros2_control = DeclareLaunchArgument(
    'use_ros2_control',
    default_value='false'
    )

    use_sim_time = LaunchConfiguration('use_sim_time')
    declare_use_sim_time = DeclareLaunchArgument(
    'use_sim_time',
    default_value='true'
    )
    #launch robot state publisher
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                    #add the use_ros2_control argument that we created in xacro and implemented in rsp.launch.py
                )]), launch_arguments={'use_sim_time': use_sim_time, 'use_ros2_control': use_ros2_control}.items()
    )




    # Include the Gazebo launch file, provided by the gazebo_ros package
    #gazebo params_file directory to increase the publish_rate
    gazebo_params_file = os.path.join(
                    get_package_share_directory(package_name),'config','gazebo_params.yaml'
                )
    gazebo_world_file = os.path.join(
                    get_package_share_directory(package_name),'worlds','maze_scale_copy.world'
                )
    
    twist_rmp_file = os.path.join(
                    get_package_share_directory(package_name),'config','twist_mux_rmp.yaml'
                )
    
    ekf_param = os.path.join(
                    get_package_share_directory(package_name),'config','ekf.yaml'
                )
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
                    launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file,
                                      'world': gazebo_world_file}.items()
             )
    depthimg_to_lsr = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(package_name), 'launch','depthimg_to_lsrscn.launch.py')]))

    merge_lsr = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(package_name), 'launch','merge_lsr.launch.py')]))

    pcl2lsr = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(package_name), 'launch','pcl2_to_lsrscn.launch.py')]))
    pcl2lsr_test = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(get_package_share_directory(package_name), 'launch','pcl2_to_lsrscn_copy.launch.py')]))


    # Run the spawner node from the gazebo_ros package. The entity name doesn't really matter if you only have a single robot.
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'my_tortoisebot',
                                   '-x', '-1.5', '-y', '1.5', '-z', '0.0',
                                   '-R', '0.0', '-P', '0.0', '-Y', '0.0'],
                        output='screen')
    

    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "diff_cont"
            # "--ros-args",
            # "-remap /diff_cont/cmd_vel_unstamped:=/cmd_vel"
        ],
        # remappings= [("/diff_cont/cmd_vel", "/cmd_vel")],
    )
    

    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_broad"],
    )



    # topic_remap = Node(
    #     package="twist_mux",
    #     executable="twist_mux",
    #     arguments=[

    #         "--ros-args",
    #         "--params-file " + twist_rmp_file,
    #         "-r /cmd_vel_out:=/diff_cont/cmd_vel_unstamped",
    #     ],

    # )
    twist_mux_node1 = Node(
            package='twist_mux',
            executable='twist_mux',
            output='screen',
            remappings={('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')},
            parameters=[twist_rmp_file],
            condition=IfCondition(use_ros2_control)
        )
    

    twist_mux_node2 = Node(
            package='twist_mux',
            executable='twist_mux',
            # name="tw_mx_2",
            output='screen',
            remappings={('/cmd_vel_out','/demo/cmd_vel')},
            parameters=[twist_rmp_file],
        )

    robot_localization_node = Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[ekf_param, {'use_sim_time': LaunchConfiguration('use_sim_time')}]
        )
    
    best_eff_conv = Node(
            package=package_name,
            executable='scan_best_effort.py'
    )

    best_eff_conv1 = Node(
            package=package_name,
            executable='scan_bsteff_test.py'
    )

    reliable_conv = Node(
            package=package_name,
            executable='scan_reliable.py'
    )

#ros2 run tf2_ros static_transform_publisher 1 2 3 0.5 0.1 -1.0 foo bar
    stp1 = Node(
        package= "tf2_ros",
        executable= "static_transform_publisher",
        name='static_transform_publisher1',

        arguments = ["0", "0", "0", "-1.57", "0", "-1.57", "camera_link_fixed", "camera_optical_link_fixed"]
    )

    stp2 = Node(
        package= "tf2_ros",
        executable= "static_transform_publisher",
        name='static_transform_publisher2',

        arguments = ["0", "0", "14.0", "0", "1.57", "0", "map", "camera_link_fixed"]
    )
    # stp3=Node(
    #     package='tf2_ros',
    #     executable='static_transform_publisher',
    #     name='static_transform_publisher3',
    #     arguments=[
    #         '--x', '0', '--y', '0', '--z', '0',
    #         '--qx', '0', '--qy', '0', '--qz', '0', '--qw', '1',
    #         '--frame-id', 'map', '--child-frame-id', 'odom'
    #     ]
    # )

    merge_lsr_fnl = IncludeLaunchDescription(PythonLaunchDescriptionSource([os.path.join(get_package_share_directory("ros2_laser_scan_merger"), 'launch','merge_scan.launch.py')]))





    # Launch them all!
    return LaunchDescription([
        # topic_remap,
        declare_use_ros2_control,
        declare_use_sim_time,
        # robot_localization_node,
        rsp,
        gazebo,
        spawn_entity,
        # diff_drive_spawner,
        # joint_broad_spawner,
        # twist_mux_node1,
        # twist_mux_node2,
        # depthimg_to_lsr,
        # merge_lsr,
        # reliable_conv,
        # best_eff_conv,
        # best_eff_conv1,
        pcl2lsr,
        # pcl2lsr_test,
        merge_lsr_fnl,
        stp1,
        stp2,
        # stp3

    ])




