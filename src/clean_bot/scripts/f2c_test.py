#!/usr/bin/env python3
# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from nav2_msgs.action import FollowPath
# from nav_msgs.msg import Path

# class Nav2ActionClient(Node):
#     def __init__(self):
#         super().__init__('nav2_action_client')
#     # # 🔥 CRITICAL FIX
#     #     self.set_parameters([
#     #     rclpy.parameter.Parameter(
#     #         'use_sim_time',
#     #         rclpy.Parameter.Type.BOOL,
#     #         True
#     #     )
#     # ])

#         self.action_client = ActionClient(self, FollowPath, 'follow_path')
#         self.path_sub = self.create_subscription(
#             Path,
#             '/coverage_path',
#             self.path_callback,
#             10
#         )
        
#     def path_callback(self , msg: Path):
#         goal_msg = FollowPath.Goal()

#         new_path = Path()
#         new_path.header.frame_id = "map"
#         new_path.header.stamp.sec = 0
#         new_path.header.stamp.nanosec = 0

#         # copy poses ONLY (ignore old header)
#         new_path.poses = msg.poses[::5]

#         goal_msg.path = new_path
#         # goal_msg.path = msg
#         goal_msg.path.header.frame_id = 'map'
#         goal_msg.path.header.stamp.nanosec = 0
#         goal_msg.path.header.stamp.sec = 0
#         goal_msg.controller_id = 'FollowPath'
#         goal_msg.goal_checker_id = 'general_goal_checker' 

        
#         self.action_client.wait_for_server()
#         future = self.action_client.send_goal_async(
#             goal_msg, feedback_callback=self.feedback_callback)
#         return future
        
#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')


# def main(args = None):
#     rclpy.init(args= args)
#     node = Nav2ActionClient()         #Modify  node_class_name heRE
#     rclpy.spin(node)
#     rclpy.shutdown()


# if __name__ == "__main__":
#     main()



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

# from geometry_msgs.msg import PoseStamped
# from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
# import rclpy

# """
# Basic navigation demo to follow a given path after smoothing
# """


# def main() -> None:
#     rclpy.init()

#     navigator = BasicNavigator()

#     # Set our demo's initial pose
#     initial_pose = PoseStamped()
#     initial_pose.header.frame_id = 'map'
#     initial_pose.header.stamp = navigator.get_clock().now().to_msg()
#     initial_pose.pose.position.x = 0.0
#     initial_pose.pose.position.y = 0.0
#     initial_pose.pose.orientation.z = 0.0
#     initial_pose.pose.orientation.w = 1.0
#     navigator.setInitialPose(initial_pose)

#     # Wait for navigation to fully activate, since autostarting nav2
#     navigator.waitUntilNav2Active()

#     # Go to our demos first goal pose
#     goal_pose = PoseStamped()
#     goal_pose.header.frame_id = 'map'
#     goal_pose.header.stamp = navigator.get_clock().now().to_msg()
#     goal_pose.pose.position.x = 7.0
#     goal_pose.pose.position.y = 0.5
#     goal_pose.pose.orientation.w = 1.0

#     # Get the path, smooth it
#     path = navigator.getPath(initial_pose, goal_pose)
#     smoothed_path = navigator.smoothPath(path)

#     # Follow path
#     follow_path_task = navigator.followPath(smoothed_path)

#     i = 0
#     while not navigator.isTaskComplete(task=follow_path_task):
#         ################################################
#         #
#         # Implement some code here for your application!
#         #
#         ################################################

#         # Do something with the feedback
#         i += 1
#         feedback = navigator.getFeedback(task=follow_path_task)
#         if feedback and i % 5 == 0:
#             print(
#                 'Estimated distance remaining to goal position: '
#                 + f'{feedback.tracking_feedback.distance_to_goal:.3f}'
#                 + '\nCurrent speed of the robot: '
#                 + f'{feedback.tracking_feedback.speed:.3f}'
#             )

#     # Do something depending on the return code
#     result = navigator.getResult()
#     if result == TaskResult.SUCCEEDED:
#         print('Goal succeeded!')
#     elif result == TaskResult.CANCELED:
#         print('Goal was canceled!')
#     elif result == TaskResult.FAILED:
#         (error_code, error_msg) = navigator.getTaskError()
#         print('Goal failed!{error_code}:{error_msg}')
#     else:
#         print('Goal has an invalid return status!')

#     navigator.lifecycleShutdown()

#     exit(0)


# if __name__ == '__main__':
#     main()


# import rclpy
# from rclpy.node import Node
# from geometry_msgs.msg import Twist, PoseStamped, PoseWithCovarianceStamped
# from nav_msgs.msg import Path
# import math


# class SimpleWaypointFollower(Node):
#     def __init__(self):
#         super().__init__('simple_waypoint_follower')
#         self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
#         self.odom_sub = self.create_subscription(PoseWithCovarianceStamped, '/amcl_pose', self.odom_callback, 10)
#         self.path_sub = self.create_subscription(Path, '/coverage_path', self.path_callback, 10)

#         self.pose = None
#         self.waypoints = []
#         self.current_index = 0
#         self.state = 'rotate'
#         self.timer = self.create_timer(0.1, self.control_loop)

#         self.move_duration = 0.0
#         self.move_start_time = None

#     def odom_callback(self, msg):
#         self.pose = msg.pose.pose

#     def path_callback(self, msg):
#         if len(msg.poses) > 0 and not self.waypoints:
#             self.waypoints = msg.poses
#             self.current_index = 0
#             self.state = 'rotate'
#             self.get_logger().info(f"📍 Received {len(msg.poses)} waypoints.")

#     def control_loop(self):
#         if not self.pose or self.current_index >= len(self.waypoints):
#             return

#         current = self.pose.position
#         orientation = self.pose.orientation
#         yaw = self.get_yaw_from_quaternion(orientation)

#         target_pose = self.waypoints[self.current_index].pose
#         target = target_pose.position
#         target_yaw = self.get_yaw_from_quaternion(target_pose.orientation)

#         dx = target.x - current.x
#         dy = target.y - current.y
#         distance = math.hypot(dx, dy)
#         angle_to_target = math.atan2(dy, dx)
#         angle_diff = self.normalize_angle(angle_to_target - yaw)
#         final_angle_diff = self.normalize_angle(target_yaw - yaw)

#         cmd = Twist()

#         if self.state == 'rotate':
#             if abs(angle_diff) > 0.1:
#                 cmd.angular.z = 1.0 * angle_diff
#                 self.get_logger().info(f"🔁 Rotating to face waypoint: angle_diff={angle_diff:.2f}")
#             else:
#                 self.get_logger().info("✅ Facing waypoint. Driving...")
#                 self.move_duration = distance / 0.2  # estimate time to reach
#                 self.move_start_time = self.get_clock().now().seconds_nanoseconds()[0]
#                 self.state = 'drive'

#         elif self.state == 'drive':
#             elapsed = self.get_clock().now().seconds_nanoseconds()[0] - self.move_start_time
#             if elapsed < self.move_duration:
#                 cmd.linear.x = 0.2
#                 self.get_logger().info(f"🚗 Driving for {elapsed:.1f}/{self.move_duration:.1f} seconds")
#             else:
#                 self.get_logger().info("🛑 Finished drive duration. Rotating to final orientation...")
#                 self.state = 'final_rotate'

#         elif self.state == 'final_rotate':
#             if abs(final_angle_diff) > 0.1:
#                 cmd.angular.z = 1.0 * final_angle_diff
#                 self.get_logger().info(f"🧭 Rotating to goal orientation: diff={final_angle_diff:.2f}")
#             else:
#                 self.get_logger().info(f"✅ Waypoint {self.current_index + 1}/{len(self.waypoints)} complete.")
#                 self.current_index += 1
#                 self.state = 'rotate'

#         self.cmd_pub.publish(cmd)

#     def get_yaw_from_quaternion(self, q):
#         siny_cosp = 2.0 * (q.w * q.z + q.x * q.y)
#         cosy_cosp = 1.0 - 2.0 * (q.y * q.y + q.z * q.z)
#         return math.atan2(siny_cosp, cosy_cosp)

#     def normalize_angle(self, angle):
#         while angle > math.pi:
#             angle -= 2 * math.pi
#         while angle < -math.pi:
#             angle += 2 * math.pi
#         return angle


# def main(args=None):
#     rclpy.init(args=args)
#     node = SimpleWaypointFollower()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()


# import rclpy
# from rclpy.node import Node
# from rclpy.action import ActionClient
# from nav2_msgs.action import FollowPath
# from nav_msgs.msg import Path
# from copy import deepcopy
# from geometry_msgs.msg import PoseWithCovarianceStamped
# from geometry_msgs.msg import PoseStamped

# class Nav2ActionClient(Node):
#     def __init__(self):
#         super().__init__('nav2_action_client')
#         self.action_client = ActionClient(self, FollowPath, 'follow_path')
#         self._path_sub = self.create_subscription(Path, "/coverage_path", self.send_goal, 10 )
        
#     def send_goal(self , msg : Path):
#         goal_msg = FollowPath.Goal()
#         goal_msg.path.poses = msg.poses
#         msg.header.stamp.sec = 0
#         msg.header.stamp.nanosec = 0
#         msg.header.frame_id = "map"
#         goal_msg.path.header.frame_id = 'map'
#         goal_msg.path.header.stamp.sec = 0
#         goal_msg.path.header.stamp.nanosec = 0
    
#         goal_msg.controller_id = 'FollowPath'
#         goal_msg.goal_checker_id = '' 
        
#         self.action_client.wait_for_server()
#         future = self.action_client.send_goal_async(
#             goal_msg, feedback_callback=self.feedback_callback)
#         return future
        
#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')

# def main(args=None):
#     rclpy.init(args=args)
#     node = Nav2ActionClient()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()


# class Nav2ActionClient(Node):
#     def __init__(self):
#         super().__init__('nav2_action_client')

#         self.action_client = ActionClient(self, FollowPath, 'follow_path')
#         self.action_client.wait_for_server()
#         print("client received now")
#         self.robot_pose = None
#         self.goal_in_progress = False

#         self._path_sub = self.create_subscription(
#             Path,
#             "/coverage_path",
#             self.send_goal,
#             10
#         )

        # self.pose_sub = self.create_subscription(
        #     PoseWithCovarianceStamped,
        #     "/amcl_pose",
        #     self.pose_callback,
        #     10
        # )

#     def pose_callback(self, msg: PoseWithCovarianceStamped):
#         if self.robot_pose is None:
#             print("appending initial pose!!")
#             self.robot_pose = msg.pose.pose

#     def send_goal(self, msg: Path):
#         if self.robot_pose is not None:

#             if self.goal_in_progress:
#                 return

#             if len(msg.poses) < 2:
#                 self.get_logger().error("Path too short!")
#                 return

#             goal_msg = FollowPath.Goal()

#             new_path = Path()
#             new_path.header.frame_id = "map"
#             new_path.header.stamp.sec = 0
#             new_path.header.stamp.nanosec = 0


#             # 1. add robot pose FIRST
#             if self.robot_pose:
#                 first_pose = PoseStamped()
#                 first_pose.header.frame_id = "map"
#                 first_pose.pose = self.robot_pose
#                 new_path.poses.append(first_pose)

#             # 2. then append rest
#             for pose in msg.poses:
#                 new_pose = deepcopy(pose)

#                 new_pose.header.stamp.sec = 0
#                 new_pose.header.stamp.nanosec = 0
#                 new_pose.header.frame_id = "map"
#                 new_path.poses.append(new_pose)


        
#             first = new_path.poses[0].pose.position
        
#             last = new_path.poses[-1].pose.position

#             self.get_logger().info(f"Start: {first.x:.2f}, {first.y:.2f}")
#             self.get_logger().info(f"End: {last.x:.2f}, {last.y:.2f}")

#             self.get_logger().info(f"Sending path with {len(new_path.poses)} poses")

#             goal_msg.path = new_path

#             self.goal_in_progress = True

#             self._send_goal_future = self.action_client.send_goal_async(goal_msg)

#     def goal_response_callback(self, future):
#         goal_handle = future.result()

#         if not goal_handle.accepted:
#             self.get_logger().error("Goal rejected")
#             self.goal_in_progress = False
#             return

#         self.get_logger().info("Goal accepted")

#         self._result_future = goal_handle.get_result_async()
#         self._result_future.add_done_callback(self.result_callback)

#     def result_callback(self, future):
#         self.get_logger().info("Path execution finished")
#         self.goal_in_progress = False

#     def feedback_callback(self, feedback_msg):
#         pass

# def main(args=None):
#     rclpy.init(args=args)
#     node = Nav2ActionClient()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()

    # # ===== follow_path action =====
    # def send_path(self, path_msg: Path, controller_id: str, goal_checker_id: str):
    #     if not self._client.wait_for_server(timeout_sec=2.0):
    #         raise RuntimeError("`/follow_path` action server not available.")

    #     goal = FollowPath.Goal()
    #     goal.path = path_msg
    #     goal.controller_id = controller_id
    #     goal.goal_checker_id = goal_checker_id

    #     with self._traj_lock:
    #         self._active_traj = controller_id
    #         # 手法切替時はその手法の軌跡をクリアして「新しい走行」として描く
    #         self._traj_points[controller_id] = []
    #         self._recording = True

    #     send_future = self._client.send_goal_async(goal, feedback_callback=self._feedback_cb)

    #     def _goal_response_cb(fut):
    #         self._current_goal_handle = fut.result()
    #         if not self._current_goal_handle.accepted:
    #             self.get_logger().warn('Goal rejected by controller_server.')
    #             # 受理されなかったら記録OFFに戻す
    #             with self._traj_lock:
    #                 self._recording = False
    #             return
    #         self.get_logger().info(f'Goal accepted by controller "{controller_id}".')
    #         self._current_goal_handle.get_result_async().add_done_callback(self._result_cb)

    #     send_future.add_done_callback(_goal_response_cb)

    

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import FollowPath
from nav_msgs.msg import Path
from rclpy.qos import QoSDurabilityPolicy, QoSHistoryPolicy, QoSReliabilityPolicy,QoSLivelinessPolicy
from rclpy.qos import QoSProfile
from geometry_msgs.msg import PoseWithCovarianceStamped
from geometry_msgs.msg import PoseStamped

class Nav2ActionClient(Node):
    def __init__(self):
        super().__init__('nav2_action_client')
        self.path_received = False  # <-- added flag
        self.paths = []
        self.home_pose = None
        self.path = None
        self.test_path = []
        amcl_pose_qos = QoSProfile(
          durability=QoSDurabilityPolicy.TRANSIENT_LOCAL,
          liveliness=QoSLivelinessPolicy.AUTOMATIC,
          reliability=QoSReliabilityPolicy.RELIABLE,
          history=QoSHistoryPolicy.KEEP_LAST,
          depth=5)
        self.action_client = ActionClient(self, FollowPath, 'follow_path')
        self._path_sub = self.create_subscription(
            Path,
            "/coverage_path",
            self.path_callback,
            10
        )


        self.pose_sub = self.create_subscription(
            PoseWithCovarianceStamped,
            "/amcl_pose",
            self._amclPoseCallback,
            amcl_pose_qos
        )

    
    def _amclPoseCallback(self, msg):
        if self.home_pose is None:
            self.home_pose = msg
            print("receibed amcl posess")
            return

    def path_callback(self, msg: Path):

        if self.path_received:
            return  # <-- ignore updates after first one

        if len(msg.poses) < 2:
            self.get_logger().warn("Received too few waypoints to follow.")
            return
        print(f" posemsgis:  {msg.poses} finished")
        path = Path()


    
        
        self.path_received = True  # <-- prevent future updates

        path.header.frame_id = "map"
        for pts in msg.poses:
            # pts = PoseStamped()
            ps = PoseStamped()
            ps.header.frame_id = "map"
            ps.pose.position.x = pts.pose.position.x
            ps.pose.position.y = pts.pose.position.y
            ps.pose.orientation.z = 0.0
            ps.pose.orientation.w = 1.0
            path.poses.append(ps)
        self.paths.append(path)
        print(type(self.paths[0]))


    def send_goal(self):
        if self.path_received:
            print("starting follow points")
            # self.home_pose = PoseWithCovarianceStamped()
            home_pt = PoseStamped()
            home_pt.header.frame_id = "map"
            home_pt.pose.position.x = self.home_pose.pose.pose.position.x
            home_pt.pose.position.y = self.home_pose.pose.pose.position.y
            home_pt.pose.orientation.z = self.home_pose.pose.pose.orientation.z
            home_pt.pose.orientation.w = self.home_pose.pose.pose.orientation.w


            # self.paths[0].poses.insert(0, home_pt)
            print(self.paths[0].poses[0].pose.position)
            print(self.paths[0].poses[1].pose.position)

            print(self.home_pose.pose.pose.position)
            now = self.get_clock().now().to_msg()

            goal_msg = FollowPath.Goal()
            goal_msg.path.header.frame_id = 'map'
            # print(type(self.paths[0]))
            # goal_msg.path = self.paths[0]
            goal_msg.path.poses = self.test_path
            goal_msg.path.header.stamp = now
            goal_msg.controller_id = 'FollowPath'
            goal_msg.goal_checker_id = '' 
            
            self.action_client.wait_for_server()
            self.send_goal_future = self.action_client.send_goal_async(
                goal_msg, feedback_callback=self.feedback_callback)
            rclpy.spin_until_future_complete(self, self.send_goal_future)
            # return future
            self.goal_handle = self.send_goal_future.result()
            self.result_future = self.goal_handle.get_result_async()
            rclpy.spin_until_future_complete(self, self.result_future)
            result_future = self.result_future.result()
            print(result_future)
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')
        # pass

# def main(args=None):
#     rclpy.init(args=args)
#     node = Nav2ActionClient()
#     node.send_goal()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()

# def main():
#     rclpy.init();
    
#     node = Nav2ActionClient()
#     while rclpy.ok() and (node.home_pose is None or node.path_received is None):
#         # We use a small timeout to keep the loop responsive
#         print('spin once')
#         rclpy.spin_once(node, timeout_sec=1.0)
#     # node.send_goal()
    
#     rclpy.shutdown()
def main(args=None):
    rclpy.init(args=args)
    node = Nav2ActionClient()

    while rclpy.ok() and (not node.path_received or node.home_pose is None):
        rclpy.spin_once(node)

    node.send_goal()
    rclpy.spin(node)

if __name__ == '__main__':
    main()

