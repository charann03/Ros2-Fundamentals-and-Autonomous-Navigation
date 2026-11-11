#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointCloud
from sensor_msgs_py import point_cloud2
from std_msgs.msg import Header


class PointCloudConverter(Node):

    def __init__(self):
        super().__init__('pointcloud_converter')

        self.sub = self.create_subscription(
            PointCloud2,
            '/camera/points',
            self.callback,
            10
        )

        self.pub = self.create_publisher(
            PointCloud,
            '/converted_cloud',
            10
        )

    def callback(self, msg):

        # Read XYZ points
        points = list(point_cloud2.read_points(
            msg,
            field_names=("x", "y", "z"),
            skip_nans=True
        ))

        # Example processing (shift points)
        processed_points = []
        for x, y, z in points:
            processed_points.append((x, y, z + 0.1))

        # Create new header
        header = Header()
        header.stamp = self.get_clock().now().to_msg()
        header.frame_id = msg.header.frame_id

        # Create new PointCloud2
        new_cloud = point_cloud2.create_cloud_xyz32(
            header,
            processed_points
        )

        # Publish
        self.pub.publish(new_cloud)


def main(args=None):
    rclpy.init(args=args)
    node = PointCloudConverter()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
