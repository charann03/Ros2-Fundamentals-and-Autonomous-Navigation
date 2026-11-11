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
from nav_msgs.msg import Path
from rclpy.node import Node

"""
Basic navigation demo to follow a given path after smoothing
"""


class FollowPath(Node):

    def __init__(self):

        super().__init__('FollowPather_Node')

        self.path_received = False
        self.latest_path = None

        self.path_sub = self.create_subscription(
            Path,
            '/coverage_path',
            self.path_callback,
            10
        )

    def path_callback(self , msg : Path):
        if self.path_received:
            return
        self.path_received = True
        self.latest_path = msg.poses
        




def main() -> None:
    rclpy.init()
    node = FollowPath()
    while node.latest_path is None:
        rclpy.spin_once(node, timeout_sec=0.1)

    # print("Path frame:", node.latest_path.header.frame_id)
    print("Num poses:", len(node.latest_path))

    navigator = BasicNavigator()
    # Set initial pose (Node 0)
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

    # Wait for Nav2
    print(len(node.latest_path))

    navigator.waitUntilNav2Active()





    try:
        for i in range(len(node.latest_path)):

            goal_pose1 = PoseStamped()
            goal_pose1.header.frame_id = 'map'
            goal_pose1.header.stamp = navigator.get_clock().now().to_msg()

            goal_pose1.pose.position.x = node.latest_path[i].pose.position.x
            goal_pose1.pose.position.y = node.latest_path[i].pose.position.y

            goal_pose1.pose.orientation.w = 1.0


            goal_pose2 = PoseStamped()
            goal_pose2.header = goal_pose1.header

            goal_pose2.pose.position.x = node.latest_path[i+1].pose.position.x
            goal_pose2.pose.position.y = node.latest_path[i+1].pose.position.y
            # if IndexError:
            #     break

            goal_pose2.pose.orientation.w = 1.0

            # Get the path, smooth it
            path = navigator.getPath(goal_pose1, goal_pose2)
            print(len(path.poses))
            # smoothed_path = navigator.smoothPath(path)
            # print(len(smoothed_path.poses))
            # Follow path
            follow_path_task = navigator.followPath(path)

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

    except IndexError:
        navigator.lifecycleShutdown()

        exit(0)



if __name__ == '__main__':
    main()