#!/usr/bin/env python3
# import rclpy
# from rclpy.node import Node
# from visualization_msgs.msg import Marker, MarkerArray
# from geometry_msgs.msg import Point
# from nav_msgs.msg import Path
# from geometry_msgs.msg import PoseStamped
# from rclpy.qos import QoSProfile, QoSDurabilityPolicy



# class MyNoDe(Node):  #Modify node_class_name heRe

#     def __init__(self):
#         super().__init__("PathToRouteNode")   #Modify node_mame heRe
#         # self.marker_pub = self.create_publisher(Marker, "/vis_marker", 10)
#         # self.timer = self.create_timer(
#         #     0.1,
#         #     self.PubMarker
#         # )
#         qos = QoSProfile(depth=1)
#         qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
#         self.marker_arr_pub = self.create_publisher(MarkerArray, "/route_graph", qos)
#         # self.timer = self.create_timer(
#         #     0.1,
#         #     self.PubMarkerArray
#         # )
#         self.path_received = False
#         self.f2c_path_sub = self.create_subscription(Path, "/coverage_path", self.pathtoroute, 10)
#         self.latest_route = None
#         self.timer = self.create_timer(0.1, self.publish_continuous_path)

#     def publish_continuous_path(self):
#         if self.latest_route is not None:
#             # self.latest_path.header.stamp = self.get_clock().now().to_msg()
#             self.marker_arr_pub.publish(self.latest_route)
#             # print("Re-published latest path")


#     # def PubMarker(self):
#     #     # shape = Marker.CUBE
#     #     # marker = Marker()
#     #     # marker.header.frame_id = "map"
#     #     # marker.header.stamp = self.get_clock().now().to_msg()
#     #     # marker.ns = "custom_shape"
#     #     # marker.id = 6
#     #     # marker.type = shape
#     #     # marker.action = Marker.ADD
#     #     # marker.pose.position.x = 1.0
#     #     # marker.pose.position.y = 1.0
#     #     # marker.pose.position.z = 0.0 
#     #     # marker.pose.orientation.x = 0.0
#     #     # marker.pose.orientation.y = 0.0
#     #     # marker.pose.orientation.z = 0.0
#     #     # marker.pose.orientation.w = 1.0
#     #     # marker.scale.x = 0.05
#     #     # marker.scale.y = 0.05
#     #     # marker.scale.z = 0.05
#     #     # marker.color.r = 0.0
#     #     # marker.color.g = 1.0
#     #     # marker.color.b = 0.0
#     #     # marker.color.a = 1.0
#     #     # # marker.lifetime.nanosec = 0
#     #     # # marker.lifetime.sec = 0
#     #     # self.marker_pub.publish(marker)

#     #     self.points = Marker()
#     #     self.line_strip = Marker()

#     #     self.points.header.frame_id = self.line_strip.header.frame_id = "map"
#     #     self.points.header.stamp = self.line_strip.header.stamp = self.get_clock().now().to_msg()
#     #     self.points.ns = self.line_strip.ns = "points_and_lines"
#     #     self.points.id = 0
#     #     self.line_strip.id = 1
#     #     self.points.type = Marker.POINTS
#     #     self.line_strip.type = Marker.LINE_STRIP
#     #     self.points.scale.x = 0.05
#     #     self.points.scale.y = 0.05

#     #     self.line_strip.scale.x = 0.05
#     #     self.points.color.g = 1.0
#     #     self.points.color.a = 1.0

#     #     self.line_strip.color.b = 1.0
#     #     self.line_strip.color.a = 1.0
#     #     self.points_list = [(-2.1,2.3,0.0), (-2.6,0.3,0.0)]
#     #     for pnt in self.points_list:
#     #         p = Point()

#     #         p.x = pnt[0]
#     #         p.y = pnt[1]
#     #         p.z = pnt[2]
#     #         self.points.points.append(p)

#     #         self.line_strip.points.append(p)
#     #     self.marker_pub.publish(self.points)
#     #     self.marker_pub.publish(self.line_strip)

#     def pathtoroute(self, msg: Path):

#         if self.path_received:
#             return

#         self.path_received = True

#         self.get_logger().info(
#             f"Received path with {len(msg.poses)} poses"
#         )

#         points = Marker()
#         line_strip = Marker()

#         points.header.frame_id = "map"
#         line_strip.header.frame_id = "map"

#         points.header.stamp = self.get_clock().now().to_msg()
#         line_strip.header.stamp = self.get_clock().now().to_msg()

#         points.ns = "route"
#         line_strip.ns = "route"

#         points.id = 0
#         line_strip.id = 1


#         points.type = Marker.POINTS
#         line_strip.type = Marker.LINE_STRIP

#         points.action = Marker.ADD
#         line_strip.action = Marker.ADD

#         points.scale.x = 0.05
#         points.scale.y = 0.05

#         line_strip.scale.x = 0.05

#         points.color.g = 1.0
#         points.color.a = 1.0

#         line_strip.color.b = 1.0
#         line_strip.color.a = 1.0

#         for pose in msg.poses:

#             p = Point()

#             p.x = pose.pose.position.x
#             p.y = pose.pose.position.y
#             p.z = 0.0

#             points.points.append(p)
#             line_strip.points.append(p)

#         # self.marker_pub.publish(points)
#         # self.marker_pub.publish(line_strip)
#         mkr_arr = MarkerArray()
#         mkr_arr.markers.append(points)
#         mkr_arr.markers.append(line_strip)
#         self.latest_route = mkr_arr
#         self.marker_arr_pub.publish(mkr_arr)
        

#     # def PubMarkerArray(self):
#     #     mkr_arr = MarkerArray()
#     #     mkr_arr.markers.append(self.points)
#     #     mkr_arr.markers.append(self.line_strip)
#     #     self.marker_arr_pub.publish(mkr_arr)





# def main(args = None):
#     rclpy.init(args= args)
#     node = MyNoDe()         #Modify  node_class_name heRE
#     # node.PubMarker()
#     rclpy.spin(node)
#     rclpy.shutdown()


# if __name__ == "__main__":
#     main()

import json

import rclpy
from rclpy.node import Node

from nav_msgs.msg import Path


class PathToRouteGraph(Node):

    def __init__(self):

        super().__init__("path_to_route_graph")

        self.path_received = False

        self.path_sub = self.create_subscription(
            Path,
            "/coverage_path",
            self.path_callback,
            10
        )

        self.output_file = "route_graph.geojson"

        self.get_logger().info(
            "Waiting for coverage path..."
        )

    def path_callback(self, msg: Path):

        if self.path_received:
            return

        self.path_received = True

        self.get_logger().info(
            f"Received path with {len(msg.poses)} poses"
        )

        features = []

        # ---------------------------
        # Create Route Nodes
        # ---------------------------
        print(msg.poses[0])
        print(msg.poses[len(msg.poses)-1])

        for node_id, pose in enumerate(msg.poses):


            x = pose.pose.position.x
            y = pose.pose.position.y

            node_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        float(x),
                        float(y)
                    ]
                },
                "properties": {
                    "frame": "map",
                    "id": node_id
                }
            }

            features.append(node_feature)

        # ---------------------------
        # Create Route Edges
        # ---------------------------

        edge_id = len(msg.poses)

        for i in range(len(msg.poses) - 1):

            edge_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "MultiLineString"
                },
                "properties": {
                    "cost": 0.0,
                    "endid": i + 1,
                    "id": edge_id,
                    "overridable": True,
                    "startid": i
                }
            }

            features.append(edge_feature)

            edge_id += 1

        # ---------------------------
        # Build GeoJSON
        # ---------------------------

        geojson = {
            "crs": {
                "properties": {
                    "name": "urn:ogc:def:crs:EPSG::3857"
                },
                "type": "name"
            },
            "features": features,
            "name": "graph",
            "type": "FeatureCollection"
        }

        # ---------------------------
        # Save File
        # ---------------------------

        with open(self.output_file, "w") as f:
            json.dump(
                geojson,
                f,
                indent=2
            )

        self.get_logger().info(
            f"Saved graph to {self.output_file}"
        )


def main(args=None):

    rclpy.init(args=args)

    node = PathToRouteGraph()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == "__main__":
    main()


