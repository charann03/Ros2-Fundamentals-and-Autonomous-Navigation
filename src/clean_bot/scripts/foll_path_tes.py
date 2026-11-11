#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
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

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy

"""
Basic navigation demo to follow a given path after smoothing
"""


def main() -> None:
    rclpy.init()

    navigator = BasicNavigator()

    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()

    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0

    initial_pose.pose.orientation.x = 0.0
    initial_pose.pose.orientation.y = 0.0
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 1.0

    navigator.setInitialPose(initial_pose)
    
    navigator.waitUntilNav2Active()
    goal_pose1 = PoseStamped()
    goal_pose1.header.frame_id = 'map'
    goal_pose1.header.stamp = navigator.get_clock().now().to_msg()

    goal_pose1.pose.position.x = -0.04303000122308731
    goal_pose1.pose.position.y = 0.1590770035982132

    goal_pose1.pose.orientation.w = 1.0


    goal_pose2 = PoseStamped()
    goal_pose2.header = goal_pose1.header

    goal_pose2.pose.position.x = 2.2197110652923584
    goal_pose2.pose.position.y = 0.03638499975204468

    goal_pose2.pose.orientation.w = 1.0

    # Get the path, smooth it
    path = navigator.getPath(goal_pose1, goal_pose2)
    print(len(path.poses))
    smoothed_path = navigator.smoothPath(path)
    print(len(smoothed_path.poses))
    # Follow path
    follow_path_task = navigator.followPath(smoothed_path)

    i = 0
    while not navigator.isTaskComplete(task=follow_path_task):
        ################################################
        #
        # Implement some code here for your application!
        #
        ################################################

        # Do something with the feedback
        i += 1
        feedback = navigator.getFeedback(task=follow_path_task)
        if feedback and i % 5 == 0:
            print(
                'Estimated distance remaining to goal position: '
                + f'{feedback.distance_to_goal:.3f}'
                + '\nCurrent speed of the robot: '
                + f'{feedback.speed:.3f}'
            )

    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        (error_code, error_msg) = navigator.getTaskError()
        print('Goal failed!{error_code}:{error_msg}')
    else:
        print('Goal has an invalid return status!')

    navigator.lifecycleShutdown()

    exit(0)


if __name__ == '__main__':
    main()