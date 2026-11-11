#! /usr/bin/env python3


import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener


class Dock_Pose_Detect(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("dock_pose_detect_node")   #Modify node_mame heRe
        self.declare_parameter("parent_frame", "camera_optical_link")
        self.declare_parameter("child_frame", "tag36h11:56")
        self.declare_parameter("publish_rate", 0.1)

        self.parent_frame = self.get_parameter("parent_frame").value
        self.child_frame = self.get_parameter("child_frame").value
        self.publish_rate = self.get_parameter("publish_rate").value

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.dock_pose_pub = self.create_publisher(PoseStamped, "/detected_dock_pose", 10)

        self.pub_pose_timer = self.create_timer(self.publish_rate, self.timer_callback)

        self.get_logger().info(f"Detected dock pose publisher initialized with parent frame: {self.parent_frame} and child frame: {self.child_frame}")


    def timer_callback(self):
        dock_pose = PoseStamped()
        dock_pose.header.stamp = self.get_clock().now().to_msg()
        dock_pose.header.frame_id = self.parent_frame
        try:
            transform = self.tf_buffer.lookup_transform(
                self.parent_frame,
                self.child_frame,
                rclpy.time.Time()
            )               
            dock_pose.pose.position.x = transform.transform.translation.x
            dock_pose.pose.position.y = transform.transform.translation.y
            dock_pose.pose.position.z = transform.transform.translation.z

            dock_pose.pose.orientation = transform.transform.rotation
            self.dock_pose_pub.publish(dock_pose)

        except TransformException as ex :
            self.get_logger().debug(f"Could not get transform: {ex}")
            return
        








def main(args = None):
    rclpy.init(args= args)
    node = Dock_Pose_Detect()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




