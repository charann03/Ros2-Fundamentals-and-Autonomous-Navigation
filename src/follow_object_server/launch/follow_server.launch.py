#!/usr/bin/env python3

# Copyright (c) 2024 Open Navigation LLC
# Copyright (c) 2024 Alberto J. Tudela Roldán
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription , TimerAction

from launch import LaunchDescription
from launch_ros.actions import Node



def generate_launch_description():
    params_dir = os.path.join(get_package_share_directory('follow_object_server'), 'params')
    package_name = "follow_object_server"
    params_file = os.path.join(params_dir, 'follow_server.yaml')
    april_tag_param =  os.path.join(get_package_share_directory("follow_object_server"), 'params', 'tag_36h11.yaml')
    following_server = Node(
        package='opennav_following',
        executable='opennav_following',
        name='following_server',
        output='screen',
        parameters=[params_file]
    )

    # controller_server = Node(
    #     package="nav2_controller",
    #     executable="controller_server",
    #     name='controller_server',
    #     output = 'screen',
    #     parameters=[params_file]
    # )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_following',
        output='screen',
        parameters=[{'autostart': True}, {'use_sim_time': True},
                    {'node_names': ['following_server']}],
    )

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
        executable="artag_pose.py",
        parameters=[{
            'use_sim_time': True,
            # 'parent_frame': "camera_optical_link",
            'parent_frame': "base_link",
            'child_frame': "tag36h11:0",
            'publish_rate': 0.1        }])
    
    follow_object_client = Node(
        package=package_name,
        executable="follow_object_client.py"
    )

    return LaunchDescription([
        following_server,
        # controller_server,
        lifecycle_manager,
        rectify_img_node,
        timer_image_view_node,
        april_tag_node,
        dock_pose_publisher,
        follow_object_client,
    ])
