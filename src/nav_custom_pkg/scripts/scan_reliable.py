#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy


class ScanRelay(Node):

    def __init__(self):
        super().__init__('scan_qos_relay')

        sub_qos = QoSProfile(depth=10)
        sub_qos.reliability = ReliabilityPolicy.BEST_EFFORT

        pub_qos = QoSProfile(depth=10)
        pub_qos.reliability = ReliabilityPolicy.RELIABLE

        self.sub = self.create_subscription(
            LaserScan,
             '/cloud_scan', #'/merged_image_scan',
            self.callback,
            sub_qos)

        self.pub = self.create_publisher(
            LaserScan,
            '/merge_scan_reliable',
            pub_qos)

    def callback(self, msg):
        self.pub.publish(msg)


def main(args = None):
    rclpy.init(args= args)
    node = ScanRelay()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()