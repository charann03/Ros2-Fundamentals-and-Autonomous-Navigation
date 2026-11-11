import os
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription , TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration , Command , TextSubstitution
from launch.actions import DeclareLaunchArgument , RegisterEventHandler
from launch_ros.actions import Node
from launch.event_handlers import OnProcessExit



def generate_launch_description():
    
    package_name= 'clean_bot_docking'
    april_tag_param = os.path.join(get_package_share_directory(package_name), 'config', 'tag_36h11.yaml')
    # tag_family = "tag_36h11"
    # tag_id = "56"
    # params_file_path = "/home/charann-inc5751/clean_bot_params_humble_main.yaml"
    params_file_path = os.path.join(get_package_share_directory(package_name), 'config', 'nav2_params_filtered_odom.yaml')




    # Process the URDF file
    # pkg_path = os.path.join(get_package_share_directory('multi_robot_description'))
    pkg_path = os.path.join(get_package_share_directory('clean_bot'))

    rectify_img_node = Node(
        package="image_proc",
        executable="rectify_node",
        remappings=[("image", "/camera/image_raw"), ("camera_info", "/camera/camera_info")]
        # remappings=[("image", "/camera/depth/image_raw"), ("camera_info", "/camera/depth/camera_info")]


    )

    image_view_node = Node(
        package="image_view",
        executable="image_view",
        remappings=[("image", "/image_rect")]
    )
    timer_image_view_node = TimerAction(
        period=3.0,
        actions=[image_view_node]
    )

    april_tag_node = Node(
        package="apriltag_ros",
        executable="apriltag_node",
        remappings=[("image_rect", "/image_rect"), ("camera_info", "/camera/camera_info")],
        # remappings=[("image_rect", "/image_rect"), ("camera_info", "/camera/depth/camera_info")],

            parameters= [april_tag_param, {'use_sim_time': True}]   )
    

    dock_pose_publisher = Node(
        package=package_name,
        executable="detected_dock_pose_publisher",
        parameters=[{
            'use_sim_time': True,
            # 'parent_frame': "camera_optical_link",
            'parent_frame': "base_link",
            'child_frame': "tag36h11:56",
            'publish_rate': 10.0
        }],
    )

    # bring_up_launch = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         [os.path.join(get_package_share_directory("nav2_bringup"), "launch", "bringup_launch.py")]),
    #         launch_arguments={
    #             "map" : os.path.join(get_package_share_directory(package_name),"maps", "cafe_world_map.yaml"),
    #             "params_file" : params_file_path,
    #             "use_sim_time" : True
    #         }.items()
    #         )

    navigation_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'bringup_launch.py')
        ),
        launch_arguments={
            'map' : os.path.join(get_package_share_directory(package_name),"maps", "cafe_world_map.yaml"),

            'use_sim_time': 'true',
            'params_file': params_file_path
        }.items()
    )



    return LaunchDescription([
        rectify_img_node,
    timer_image_view_node,
    april_tag_node,
    dock_pose_publisher,
    navigation_launch_cmd
    ])
