#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
# from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
# from nav2_msgs.action import UndockRobot
from rclpy.action import ActionClient
from action_msgs.msg import GoalStatus
from opennav_docking_msgs.action import UndockRobot
from nav2_msgs.action import NavigateToPose
# from nav_msgs.msg import Path


class undock_custom(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("undock_custom_node")   #Modify node_mame heRe
        self.goal_handle = None
        self.result_future = None
        self.status = None
        self.feedback = None
        self.dock_pose_received = False
        self.dock_pose = None
        self.staging_x_offset = 3.0

        self.undocking_client = ActionClient(self, UndockRobot,
                                            '/undock_robot')
        self.sub_dock_pose = self.create_subscription(Odometry, '/odometry/filtered', self.dock_pose_cb, 10)
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

    def dock_pose_cb(self, msg: Odometry):
        if self.dock_pose_received:
            return
        
        self.dock_pose_received = True
        self.dock_pose = PoseStamped()
        self.dock_pose.header.frame_id = "map"
        self.dock_pose.header.stamp = self.get_clock().now().to_msg()
        self.dock_pose.pose = msg.pose.pose



        self.get_logger().info(
            f"Received staging pose: "
            f"{msg.pose.pose.position.x:.2f}, "
            f"{msg.pose.pose.position.y:.2f}"
        )

    def send_goal(self, dock_pose: PoseStamped):
        goal_msg = NavigateToPose.Goal()

        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = dock_pose.pose.position.x + self.staging_x_offset
        goal_msg.pose.pose.position.y = dock_pose.pose.position.y
        goal_msg.pose.pose.orientation = dock_pose.pose.orientation

        self.action_client.wait_for_server()

        future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback)

        future.add_done_callback(self.nav_goal_response_cb)

    def nav_goal_response_cb(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Navigation goal rejected")
            rclpy.shutdown()
            return

        self.get_logger().info("Navigation goal accepted")

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.nav_result_cb)

    def nav_result_cb(self, future):
        result = future.result()
        status = result.status

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Navigation succeeded. Shutting down.")
        else:
            self.get_logger().error(
                f"Navigation failed with status {status}"
            )

        self.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')


    
    def undockRobot(self, dock_type , max_undocking_time):
        """Send a `UndockRobot` action request."""
        print("Waiting for 'UndockRobot' action server")
        while not self.undocking_client.wait_for_server(timeout_sec=1.0):
            print('"UndockRobot" action server not available, waiting...')

        goal_msg = UndockRobot.Goal()
        goal_msg.dock_type = dock_type
        goal_msg.max_undocking_time = max_undocking_time

        print('Undocking from dock of type: ' + str(dock_type) + '...')
        send_goal_future = self.undocking_client.send_goal_async(goal_msg,
                                                                 self._feedbackCallback)
        # self.send_goal_future.add_done_callback(self.result_cb)


    
        

        rclpy.spin_until_future_complete(self, send_goal_future)
        self.goal_handle = send_goal_future.result()

        if not self.goal_handle.accepted:
            print('Undocking request was rejected!')
            return False

        self.result_future = self.goal_handle.get_result_async()
        rclpy.spin_until_future_complete(self, self.result_future, timeout_sec=0.10)
        self.result_future.add_done_callback(self.result_cb)
        return True
    
    def result_cb(self, future):
        result = future.result().result
        status = self.goal_handle.status
        print(status)
        print(result)

        if self.result_future.result():
            self.status = self.result_future.result().status
            if self.status != GoalStatus.STATUS_SUCCEEDED:
                print(f'Task with failed with status code: {self.status}, going to goal pose')
                self.send_goal(self.dock_pose)
                

                return True
            
        else:
            # Timed out, still processing, not complete yet
            return False

        print('Task succeeded!')
        return True
    # def isTaskComplete(self):
    #     """Check if the task request of any type is complete yet."""
    #     if not self.result_future:
    #         # task was cancelled or completed
    #         return True
    #     rclpy.spin_until_future_complete(self, self.result_future, timeout_sec=0.10)
        # if self.result_future.result():
        #     self.status = self.result_future.result().status
        #     if self.status != GoalStatus.STATUS_SUCCEEDED:
        #         print(f'Task with failed with status code: {self.status}')
        #         return True
            
        #     if self.status == GoalStatus.STATUS_ABORTED:
        #         print("task aborted succesfuly")
        #         return True
        # else:
        #     # Timed out, still processing, not complete yet
        #     return False

        # print('Task succeeded!')
        # return True

    def _feedbackCallback(self, msg):
        self.feedback = msg.feedback
        print(self.feedback)
        return
    



def main(args=None):
    rclpy.init(args=args)

    node = undock_custom()

    print("Waiting for dock pose...")

    while rclpy.ok() and node.dock_pose is None:
        rclpy.spin_once(node, timeout_sec=0.1)

    print("Got staging pose")

    node.undockRobot('rosmaster_x3_dock', 2.0)


    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    if rclpy.ok():
        rclpy.shutdown()


if __name__ == "__main__":
    main()




