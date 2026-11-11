#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import PointCloud2
from tf2_ros import Buffer, TransformListener
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from sensor_msgs_py import point_cloud2
# from std_msgs.msg import Header

class fusion_laser_cloud(Node):  #Modify node_class_name heRe

    def __init__(self):

        super().__init__("laser_to_pointcloud")   #Modify node_mame heRe
        self.tf_buffer = None
        self.tf_listener = None
        self.latest_lidar = None
        self.latest_depth = None
        self.cloud_points_subscriber = self.create_subscription(PointCloud2, "/camera/points", self.depth_callback, 10 )
        self.laser_cloud_subscriber = self.create_subscription(PointCloud2, "/lidar_cloud", self.lidar_cloud_callback, 10)
        self.tf_buffer = Buffer()
        self.tf_listenfer = TransformListener(self.tf_buffer, self)
        self.merged_publisher = self.create_publisher(PointCloud2, "/merged_cloud", 10)


    def lidar_cloud_callback(self, lidar_cloud_msg_ : PointCloud2):
        self.get_logger().info("Lidar")
        self.latest_lidar = lidar_cloud_msg_
        self.fuse_clouds()

    def depth_callback(self, depth_msg : PointCloud2):
        self.get_logger().info("Cam")
        self.latest_depth = depth_msg
        self.fuse_clouds()

    def fuse_clouds(self):
        if self.latest_lidar == None or self.latest_depth == None:
            return

        # Transform lidar
        transform_lidar = self.tf_buffer.lookup_transform(
            self.latest_depth.header.frame_id,
            self.latest_lidar.header.frame_id,
            rclpy.time.Time()
        )

        lidar_base = do_transform_cloud(self.latest_lidar, transform_lidar)

        lidar_points = list(point_cloud2.read_points(
        lidar_base,
        field_names=("x", "y", "z"),
        skip_nans=True
        ))

        depth_points = list(point_cloud2.read_points(
        self.latest_depth,
        field_names=("x", "y", "z"),
        skip_nans=True
        ))

        merged_points = lidar_points + depth_points


        merged_cloud = point_cloud2.create_cloud_xyz32(self.latest_depth.header, merged_points)
        self.merged_publisher.publish(merged_cloud)




def main(args = None):
    rclpy.init(args= args)
    node = fusion_laser_cloud()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




