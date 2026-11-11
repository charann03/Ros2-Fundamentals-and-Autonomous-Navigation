#!/usr/bin/env python3
"""
laser_scan_merger.py
--------------------
ROS2 node that subscribes to two LaserScan topics, transforms both scans
into a common output frame via TF2, merges the point clouds, and publishes
a single merged LaserScan on /scan_merged.

Dependencies:
    ros-<distro>-laser-geometry
    ros-<distro>-tf2-sensor-msgs

Usage:
    ros2 run <your_package> laser_scan_merger \
        --ros-args \
        -p scan1_topic:=/scan_front \
        -p scan2_topic:=/scan_rear \
        -p output_frame:=base_link \
        -p angle_min:=-3.14159 \
        -p angle_max:=3.14159 \
        -p angle_increment:=0.00581 \
        -p range_min:=0.1 \
        -p range_max:=30.0
"""

import math
import numpy as np

import rclpy
from rclpy.node import Node
from rclpy.time import Time
from rclpy.duration import Duration
from rclpy.qos import QoSProfile, QoSReliabilityPolicy, QoSHistoryPolicy

from sensor_msgs.msg import LaserScan, PointCloud2
from message_filters import ApproximateTimeSynchronizer, Subscriber

import tf2_ros
import tf2_py as tf2
from tf2_sensor_msgs.tf2_sensor_msgs import do_transform_cloud
from laser_geometry import LaserProjection

try:
    import sensor_msgs_py.point_cloud2 as pc2
except ImportError:
    from sensor_msgs import point_cloud2 as pc2


class LaserScanMerger(Node):
    """Merges two LaserScan topics into one scan published in `output_frame`."""

    def __init__(self):
        super().__init__("laser_scan_merger")

        # ── Parameters ────────────────────────────────────────────────────────
        self.declare_parameter("scan1_topic",      "/scan_best_effort")
        self.declare_parameter("scan2_topic",      "/cloud_scan")
        self.declare_parameter("output_topic",     "/scan_merged")
        self.declare_parameter("output_frame",     "base_link")
        self.declare_parameter("angle_min",        -math.pi)
        self.declare_parameter("angle_max",         math.pi)
        self.declare_parameter("angle_increment",   0.005)       # ~0.29 deg
        self.declare_parameter("range_min",         0.1)
        self.declare_parameter("range_max",         30.0)
        self.declare_parameter("sync_slop",         0.05)        # seconds
        self.declare_parameter("tf_timeout",        1.0)         # seconds

        p = self.get_parameters([
            "scan1_topic", "scan2_topic", "output_topic", "output_frame",
            "angle_min", "angle_max", "angle_increment",
            "range_min", "range_max", "sync_slop", "tf_timeout",
        ])
        (
            self.scan1_topic, self.scan2_topic, self.output_topic,
            self.output_frame, self.angle_min, self.angle_max,
            self.angle_increment, self.range_min, self.range_max,
            self.sync_slop, self.tf_timeout,
        ) = [p_.value for p_ in p]

        # ── Derived geometry ───────────────────────────────────────────────────
        num_beams = int(
            round((self.angle_max - self.angle_min) / self.angle_increment)
        ) + 1
        self.num_beams = num_beams
        self.get_logger().info(
            f"Output scan: frame='{self.output_frame}', "
            f"beams={num_beams}, "
            f"angle=[{math.degrees(self.angle_min):.1f}°, "
            f"{math.degrees(self.angle_max):.1f}°], "
            f"range=[{self.range_min}, {self.range_max}]"
        )

        # ── TF2 ───────────────────────────────────────────────────────────────
        self.tf_buffer   = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)

        # ── Laser projection ──────────────────────────────────────────────────
        self.projector = LaserProjection()

        # ── QoS ───────────────────────────────────────────────────────────────
        sensor_qos = QoSProfile(
            reliability=QoSReliabilityPolicy.BEST_EFFORT,
            history=QoSHistoryPolicy.KEEP_LAST,
            depth=5,
        )

        # ── Synchronized subscribers ──────────────────────────────────────────
        self.sub1 = Subscriber(self, LaserScan, self.scan1_topic, qos_profile=sensor_qos)
        self.sub2 = Subscriber(self, LaserScan, self.scan2_topic, qos_profile=sensor_qos)

        self.sync = ApproximateTimeSynchronizer(
            [self.sub1, self.sub2],
            queue_size=10,
            slop=self.sync_slop,
        )
        self.sync.registerCallback(self.callback)

        # ── Publisher ─────────────────────────────────────────────────────────
        self.pub = self.create_publisher(LaserScan, self.output_topic, sensor_qos)

        self.get_logger().info(
            f"Merging '{self.scan1_topic}' + '{self.scan2_topic}' "
            f"→ '{self.output_topic}'"
        )

    # ── Main callback ─────────────────────────────────────────────────────────

    def callback(self, scan1: LaserScan, scan2: LaserScan):
        """Called when a synchronised pair of scans arrives."""
        stamp = scan1.header.stamp          # use scan1 timestamp for output

        # Collect all (x, y) points from both scans in the output frame
        all_points = []
        for scan in (scan1, scan2):
            pts = self._scan_to_points(scan, stamp)
            if pts is not None:
                all_points.extend(pts)

        if not all_points:
            self.get_logger().warn("No points after transform – skipping publish.")
            return

        merged = self._points_to_scan(all_points, stamp)
        self.pub.publish(merged)

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _scan_to_points(self, scan: LaserScan, target_stamp):
        """
        Project scan → PointCloud2 → transform to output_frame → list of (x,y).
        Returns None on TF failure.
        """
        # Project to 3-D point cloud (in the scan's own frame)
        cloud: PointCloud2 = self.projector.projectLaser(
            scan,
            range_cutoff=self.range_max,
            channel_options=LaserProjection.ChannelOption.NONE,
        )

        # Look up transform from scan frame → output frame
        try:
            transform = self.tf_buffer.lookup_transform(
                self.output_frame,
                scan.header.frame_id,
                Time.from_msg(scan.header.stamp),
                timeout=Duration(seconds=self.tf_timeout),
            )
        except (
            tf2_ros.LookupException,
            tf2_ros.ConnectivityException,
            tf2_ros.ExtrapolationException,
        ) as e:
            self.get_logger().warn(
                f"TF lookup failed for frame '{scan.header.frame_id}': {e}"
            )
            return None

        # Transform cloud into output frame
        cloud_transformed = do_transform_cloud(cloud, transform)

        # Extract (x, y) – ignore z (planar merge)
        points = []
        for p in pc2.read_points(cloud_transformed, field_names=("x", "y"), skip_nans=True):
            points.append((p[0], p[1]))

        return points

    def _points_to_scan(self, points, stamp) -> LaserScan:
        """
        Bin (x,y) points into the output LaserScan's angular bins.
        For each bin the *minimum* range is kept (closest obstacle wins).
        """
        ranges = np.full(self.num_beams, np.inf, dtype=np.float32)

        for x, y in points:
            angle = math.atan2(y, x)
            r     = math.hypot(x, y)

            # Skip points outside configured range
            if r < self.range_min or r > self.range_max:
                continue

            # Map angle → bin index
            idx = int(round(
                (angle - self.angle_min) / self.angle_increment
            ))
            if 0 <= idx < self.num_beams:
                if r < ranges[idx]:
                    ranges[idx] = r

        # Replace inf with range_max (standard convention for "no obstacle")
        ranges[ranges == np.inf] = self.range_max

        msg = LaserScan()
        msg.header.stamp    = stamp
        msg.header.frame_id = self.output_frame
        msg.angle_min       = float(self.angle_min)
        msg.angle_max       = float(self.angle_max)
        msg.angle_increment = float(self.angle_increment)
        msg.time_increment  = 0.0
        msg.scan_time       = 0.0
        msg.range_min       = float(self.range_min)
        msg.range_max       = float(self.range_max)
        msg.ranges          = ranges.tolist()
        msg.intensities     = []        # intensities not preserved (multi-sensor)

        return msg


# ── Entry point ───────────────────────────────────────────────────────────────

def main(args=None):
    rclpy.init(args=args)
    node = LaserScanMerger()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()