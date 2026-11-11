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
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    params_dir = os.path.join(get_package_share_directory('follow_object_server'), 'params')
    opencv_package = os.path.join(get_package_share_directory("opencv_ros2"))
    package_name = "follow_object_server"
    params_file = os.path.join(params_dir, 'follow_server.yaml')
    following_server = Node(
        package='opennav_following',
        executable='opennav_following',
        name='following_server',
        output='screen',
        parameters=[params_file]
    )

    lifecycle_manager = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager_following',
        output='screen',
        parameters=[{'autostart': True}, {'use_sim_time': True},
                    {'node_names': ['following_server']}],
    )

    object_pose_publisher = Node(
        package= "opencv_ros2",
        executable="object_pose_detection",
        parameters=[{
            'use_sim_time': True,
            # 'parent_frame': "camera_optical_link",
            'parent_frame': "base_link",
            'target_frame': "detected_object_frame",
            'publish_rate': 0.1        }])
    #launch yolo detection
    
    object_detection_yolo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [os.path.join(opencv_package, 'launch', 'master_objectdetection.launch.py')]))
    
    #publish detected object transform in here

    detected_object_transform = Node(
        package= "opencv_ros2",
        executable= "camera_to_world",
        parameters=[{"use_sim_time": True}]
    )

    # instance_1 = RegisterEventHandler(
    #     OnProcessExit(
    #         target_action=detected_object_transform,
    #         on_exit= object_detection_yolo
    #     )
    # )

    # instance_2 = RegisterEventHandler(
    #     OnProcessExit(
    #         target_action= object_pose_publisher,
    #         on_exit= detected_object_transform        )
    # )
    timer_transform_node = TimerAction(
        period=2.0,
        actions=[detected_object_transform]
    )

    timer_object_pose_pub_node = TimerAction(
        period=3.0,
        actions=[object_pose_publisher]
    )
    
    follow_object_client = Node(
        package= "follow_object_server",
        executable="follow_object_client.py",
        parameters=[{"pose_topic" : "/detected_object_pose" }]
    )

    return LaunchDescription([
        following_server,
        # controller_server,
        lifecycle_manager,
        object_detection_yolo,
        timer_transform_node,
        timer_object_pose_pub_node,

        follow_object_client,
    ])
