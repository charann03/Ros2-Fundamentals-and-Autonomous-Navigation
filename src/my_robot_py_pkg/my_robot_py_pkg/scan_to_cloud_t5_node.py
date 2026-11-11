#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud2
from laser_geometry import LaserProjection


class Scan_to_cloud(Node):  #Modify node_class_name heRe

    def __init__(self):

        super().__init__("laser_to_pointcloud")   #Modify node_mame heRe
        self.laser_subscriber = self.create_subscription(LaserScan, "/scan", self.laser_to_cloud, 10)
        self.cloud_publisher = self.create_publisher(PointCloud2, "/lidar_cloud", 10)
        self.projector = LaserProjection()

    def laser_to_cloud(self, laser_msg_:LaserScan):
        cloud_msg = self.projector.projectLaser(laser_msg_)
        self.cloud_publisher.publish(cloud_msg)
        self.get_logger().info(f"publishing {cloud_msg}")




def main(args = None):
    rclpy.init(args= args)
    node = Scan_to_cloud()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




