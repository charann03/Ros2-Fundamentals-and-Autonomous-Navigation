#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
# from nav2_msgs.action import FollowObject
from opennav_following_msgs.action import FollowObject
from builtin_interfaces.msg import Duration

class Nav2ActionClient(Node):
    def __init__(self):
        super().__init__('follow_object_node_client')
        self.action_client = ActionClient(self, FollowObject, 'follow_object')
        self.declare_parameter("pose_topic", "/detected_artag_pose")
        self.pose_topic = self.get_parameter("pose_topic").value
        
    def send_goal(self):
        goal_msg = FollowObject.Goal()
        time = Duration()
        time.sec = -1
        # Set appropriate fields for FollowObject
        goal_msg.pose_topic = self.pose_topic
        # goal_msg.tracked_frame = "tag36h11:0"
        goal_msg.max_duration = time
        
        self.action_client.wait_for_server()
        future = self.action_client.send_goal_async(
            goal_msg, feedback_callback=self.feedback_callback)
        return future
        
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')



def main(args = None):
    rclpy.init(args= args)
    node = Nav2ActionClient()         #Modify  node_class_name heRE
    node.send_goal()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()





