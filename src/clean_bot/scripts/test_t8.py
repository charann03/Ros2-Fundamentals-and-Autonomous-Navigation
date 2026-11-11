#!/usr/bin/env python3
# # import rclpy
# # from rclpy.node import Node
# # from rclpy.qos import QoSProfile, QoSDurabilityPolicy
# # from nav_msgs.msg import OccupancyGrid, Path
# # from visualization_msgs.msg import Marker
# # from geometry_msgs.msg import Point, PoseStamped
# # from builtin_interfaces.msg import Duration

# # import numpy as np
# # from scipy.ndimage import binary_dilation, label, find_objects
# # from tf_transformations import quaternion_from_euler
# # import math

# # class CoveragePlanner(Node):
# #     def __init__(self):
# #         super().__init__('coverage_planner')
# #         self.map_received = False
# #         self.robot_radius = 0.225

# #         qos = QoSProfile(depth=1)
# #         qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL

# #         self.subscription = self.create_subscription(OccupancyGrid, '/map', self.map_callback, qos)
# #         self.marker_pub = self.create_publisher(Marker, '/navigable_mask_marker', qos)
# #         self.path_pub = self.create_publisher(Path, '/coverage_path', qos)

# #         self.get_logger().info("CoveragePlanner tile sweep v1 started. Waiting for map...")

# #     def map_callback(self, msg):
# #         if self.map_received:
# #             return
# #         self.map_received = True
# #         self.get_logger().info("Map received!")

#         # grid = np.array(msg.data).reshape((msg.info.height, msg.info.width))
#         # resolution = msg.info.resolution
#         # origin_x = msg.info.origin.position.x
#         # origin_y = msg.info.origin.position.y

#         # height, width = grid.shape
#         # self.get_logger().info(f"Map size: {width}x{height}, resolution: {resolution:.3f}")

#         # free_mask = grid == 0
#         # obstacle_mask = grid == 100

#         # dilated_obstacles = binary_dilation(obstacle_mask, iterations=10,border_value=1, brute_force=True)
#         # nav_mask = np.logical_and(free_mask, ~dilated_obstacles)

#         # labeled, _ = label(nav_mask)
#         # start_x_px = int(-origin_y / resolution)
#         # start_y_px = int(-origin_x / resolution)
#         # start_x_px = np.clip(start_x_px, 0, height - 1)
#         # start_y_px = np.clip(start_y_px, 0, width - 1)
#         # robot_region = labeled[start_x_px, start_y_px]

# #         if robot_region == 0:
# #             self.get_logger().warn("Robot is not in a navigable region.")
# #             return

# #         nav_mask = labeled == robot_region
# #         self.publish_navigable_marker(nav_mask, resolution, origin_x, origin_y)

# #         visited = np.zeros_like(nav_mask, dtype=bool)
# #         all_waypoints = []
# #         max_waypoints = 1200# Cap on total waypoints

# #         while len(all_waypoints) < max_waypoints:
# #             waypoints = self.sweep_snake(nav_mask, visited, resolution, origin_x, origin_y, tile_size_m=self.robot_radius*2)
# #             if not waypoints:
# #                 break

# #             remaining = max_waypoints - len(all_waypoints)
# #             all_waypoints.extend(waypoints[:remaining])

# #             if len(all_waypoints) >= max_waypoints:
# #                 self.get_logger().warn(f"Reached max waypoint cap ({max_waypoints}). Stopping early.")
# #                 break

# #             unvisited = np.logical_and(nav_mask, ~visited)
# #             labeled_unvisited, _ = label(unvisited)
# #             slices = find_objects(labeled_unvisited)

# #             resumed = False
# #             for i, slc in enumerate(slices):
# #                 if slc is None:
# #                     continue
# #                 region = labeled_unvisited[slc] == (i + 1)
# #                 h, w = region.shape
# #                 if h >= 40 and w >= 40:
# #                     cy, cx = np.array(np.argwhere(region).mean(axis=0), dtype=int)
# #                     center_row = slc[0].start + cy
# #                     center_col = slc[1].start + cx
# #                     self.get_logger().info(f"Detected unvisited cluster at ({center_row}, {center_col}), resuming sweep...")
# #                     visited[center_row, center_col] = False
# #                     resumed = True
# #                     break
# #             if not resumed:
# #                 break

# #         self.get_logger().info(f"Planned {len(all_waypoints)} total sweep waypoints.")
# #         self.publish_path(all_waypoints)

# #     def sweep_snake(self, mask, visited, resolution, origin_x, origin_y, tile_size_m=0.25):
# #         tile_size_px = max(1, int(tile_size_m / resolution))
# #         height, width = mask.shape
# #         waypoints = []
# #         row_dirs = [(0, 1), (0, -1)]  # right, left

# #         for start_row in range(height):
# #             for start_col in range(width):
# #                 if mask[start_row, start_col] and not visited[start_row, start_col]:
# #                     row, col = start_row, start_col
# #                     break
# #             else:
# #                 continue
# #             break
# #         else:
# #             self.get_logger().warn("No navigable start point found.")
# #             return []

# #         dir_idx = 0
# #         backtrack_stack = []

# #         while True:
# #             if not mask[row, col] or visited[row, col]:
# #                 break

# #             visited[row, col] = True
# #             backtrack_stack.append((row, col))
# #             x = origin_x + col * resolution
# #             y = origin_y + row * resolution
# #             waypoints.append((x, y))

# #             dr, dc = row_dirs[dir_idx]
# #             next_r = row + dr * tile_size_px
# #             next_c = col + dc * tile_size_px

# #             if (
# #                 0 <= next_r < height and 0 <= next_c < width
# #                 and mask[next_r, next_c]
# #                 and not visited[next_r, next_c]
# #             ):
# #                 row, col = next_r, next_c
# #                 continue

# #             found = False
# #             for delta_r in range(tile_size_px, height - row, tile_size_px):
# #                 down_r = row + delta_r
# #                 if down_r >= height:
# #                     break
# #                 if mask[down_r, col] and not visited[down_r, col]:
# #                     row = down_r
# #                     dir_idx = 1 - dir_idx
# #                     found = True
# #                     break

# #             if found:
# #                 continue

# #             self.get_logger().info("Falling back to backtracking...")
# #             dir_idx = 1 - dir_idx
# #             while backtrack_stack:
# #                 b_row, b_col = backtrack_stack.pop()
# #                 down_r = b_row + tile_size_px
# #                 if (
# #                     0 <= down_r < height
# #                     and mask[down_r, b_col]
# #                     and not visited[down_r, b_col]
# #                 ):
# #                     x = origin_x + b_col * resolution
# #                     y = origin_y + b_row * resolution
# #                     waypoints.append((x, y))
# #                     row, col = down_r, b_col
# #                     self.get_logger().info("Backtracked and dropped down. Resuming sweep.")
# #                     break
# #             else:
# #                 self.get_logger().info("Backtracking failed. Ending sweep.")
# #                 break

# #         return waypoints

# #     def prune_waypoints(self, waypoints, tolerance=1e-3):
# #         if len(waypoints) <= 2:
# #             return waypoints

# #         pruned = [waypoints[0]]

# #         for i in range(1, len(waypoints) - 1):
# #             x0, y0 = pruned[-1]
# #             x1, y1 = waypoints[i]
# #             x2, y2 = waypoints[i + 1]

# #             v1 = (x1 - x0, y1 - y0)
# #             v2 = (x2 - x1, y2 - y1)

# #             cross = abs(v1[0]*v2[1] - v1[1]*v2[0])
# #             dot = v1[0]*v2[0] + v1[1]*v2[1]
# #             norm1 = math.hypot(*v1)
# #             norm2 = math.hypot(*v2)

# #             if norm1 * norm2 == 0:
# #                 pruned.append(waypoints[i])
# #                 continue

# #             sin_angle = cross / (norm1 * norm2)

# #             if abs(sin_angle) > tolerance:
# #                 pruned.append(waypoints[i])

# #         pruned.append(waypoints[-1])
# #         self.get_logger().info(f"Pruned from {len(waypoints)} to {len(pruned)} waypoints.")
# #         return pruned

# #     def publish_path(self, waypoints):
# #         if not waypoints:
# #             return

# #         pruned_waypoints = self.prune_waypoints(waypoints)

# #         now = self.get_clock().now().to_msg()
# #         path_msg = Path()
# #         path_msg.header.frame_id = "map"
# #         path_msg.header.stamp = now

# #         for i in range(len(pruned_waypoints)):
# #             x, y = pruned_waypoints[i]
# #             pose = PoseStamped()
# #             pose.header.frame_id = "map"
# #             pose.header.stamp = now
# #             pose.pose.position.x = x
# #             pose.pose.position.y = y
# #             pose.pose.position.z = 0.0

# #             if i < len(pruned_waypoints) - 1:
# #                 dx = pruned_waypoints[i + 1][0] - x
# #                 dy = pruned_waypoints[i + 1][1] - y
# #                 yaw = math.atan2(dy, dx)
# #                 q = quaternion_from_euler(0, 0, yaw)
# #                 pose.pose.orientation.x = q[0]
# #                 pose.pose.orientation.y = q[1]
# #                 pose.pose.orientation.z = q[2]
# #                 pose.pose.orientation.w = q[3]
# #             else:
# #                 pose.pose.orientation.w = 1.0

# #             path_msg.poses.append(pose)

# #         self.path_pub.publish(path_msg)
# #         self.get_logger().info(f"Published Path with {len(path_msg.poses)} poses.")

# #     def publish_navigable_marker(self, mask, resolution, origin_x, origin_y):
# #         marker = Marker()
# #         marker.header.frame_id = "map"
# #         marker.header.stamp = self.get_clock().now().to_msg()
# #         marker.ns = "coverage_debug"
# #         marker.id = 0
# #         marker.type = Marker.SPHERE_LIST
# #         marker.action = Marker.ADD
# #         marker.scale.x = resolution
# #         marker.scale.y = resolution
# #         marker.scale.z = resolution
# #         marker.color.r = 0.0
# #         marker.color.g = 1.0
# #         marker.color.b = 0.0
# #         marker.color.a = 0.8
# #         marker.lifetime = Duration(sec=0)

# #         height, width = mask.shape
# #         for row in range(height):
# #             for col in range(width):
# #                 if mask[row, col]:
# #                     pt = Point()
# #                     pt.x = origin_x + col * resolution
# #                     pt.y = origin_y + row * resolution
# #                     pt.z = 0.0
# #                     marker.points.append(pt)

# #         self.marker_pub.publish(marker)
# #         self.get_logger().info(f"Published navigable area marker with {len(marker.points)} points.")


# # def main(args=None):
# #     rclpy.init(args=args)
# #     node = CoveragePlanner()
# #     rclpy.spin(node)
# #     node.destroy_node()
# #     rclpy.shutdown()


# # if __name__ == '__main__':
# #     main()



# # import rclpy
# # from rclpy.node import Node
# # from rclpy.qos import QoSProfile, QoSDurabilityPolicy
# # from nav_msgs.msg import OccupancyGrid, Path
# # from visualization_msgs.msg import Marker
# # from geometry_msgs.msg import Point, PoseStamped
# # from builtin_interfaces.msg import Duration

# # import numpy as np
# # from scipy.ndimage import binary_dilation, label
# # from tf_transformations import quaternion_from_euler
# # import math


# # class CoveragePlanner(Node):
# #     def __init__(self):
# #         super().__init__('coverage_planner')

# #         self.robot_radius = 0.225
# #         self.map_received = False

# #         qos = QoSProfile(depth=1)
# #         qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL

# #         self.create_subscription(OccupancyGrid, '/map', self.map_callback, qos)
# #         self.path_pub = self.create_publisher(Path, '/coverage_path', qos)
# #         self.marker_pub = self.create_publisher(Marker, '/navigable_mask_marker', qos)

# #         self.get_logger().info("Optimized Coverage Planner Started")

# #     # ========================= MAP CALLBACK =========================
# #     def map_callback(self, msg):
# #         if self.map_received:
# #             return
# #         self.map_received = True

# #         grid = np.array(msg.data).reshape((msg.info.height, msg.info.width))
# #         resolution = msg.info.resolution
# #         origin_x = msg.info.origin.position.x
# #         origin_y = msg.info.origin.position.y

# #         height, width = grid.shape
# #         self.get_logger().info(f"Map size: {width}x{height}, resolution: {resolution:.3f}")


# #         free = grid == 0
# #         obstacles = grid == 100

# #         # Inflate obstacles (safety buffer)
# #         dilated = binary_dilation(obstacles, iterations=10,border_value=1, brute_force=True)
# #         nav_mask = np.logical_and(free, ~dilated)

# #         # Keep only reachable region
# #         labeled, _ = label(nav_mask)
# #         start_r = int(-origin_y / resolution)
# #         start_c = int(-origin_x / resolution)
# #         start_r = np.clip(start_r, 0, nav_mask.shape[0] - 1)
# #         start_c = np.clip(start_c, 0, nav_mask.shape[1] - 1)

# #         region_id = labeled[start_r, start_c]
# #         nav_mask = labeled == region_id

# #         self.publish_marker(nav_mask, resolution, origin_x, origin_y)

# #         # ========================= NEW OPTIMAL PLANNER =========================
# #         lanes = self.generate_lanes(
# #             nav_mask,
# #             resolution,
# #             origin_x,
# #             origin_y,
# #             step_m=self.robot_radius * 2
# #         )

# #         waypoints = self.zigzag_order(lanes)

# #         self.get_logger().info(f"Generated {len(waypoints)} optimized waypoints")
# #         self.publish_path(waypoints)

# #     # ========================= LANE GENERATION =========================
# #     def generate_lanes(self, mask, resolution, origin_x, origin_y, step_m):
# #         step_px = max(1, int(step_m / resolution))
# #         height, width = mask.shape

# #         lanes = []

# #         for row in range(0, height, step_px):
# #             cols = np.where(mask[row])[0]
# #             if len(cols) == 0:
# #                 continue

# #             # Split segments to avoid obstacles
# #             splits = np.where(np.diff(cols) != 1)[0] + 1
# #             segments = np.split(cols, splits)

# #             for seg in segments:
# #                 start = seg.min()
# #                 end = seg.max()

# #                 x1 = origin_x + start * resolution
# #                 x2 = origin_x + end * resolution
# #                 y = origin_y + row * resolution

# #                 lanes.append([(x1, y), (x2, y)])

# #         return lanes

# #     # ========================= ZIGZAG ORDER =========================
# #     def zigzag_order(self, lanes):
# #         ordered = []
# #         direction = 1

# #         for lane in lanes:
# #             if direction == 1:
# #                 ordered.extend(lane)
# #             else:
# #                 ordered.extend(lane[::-1])

# #             direction *= -1

# #         return ordered

# #     # ========================= PATH PUBLISH =========================
# #     def publish_path(self, waypoints):
# #         if not waypoints:
# #             return

# #         path = Path()
# #         path.header.frame_id = "map"
# #         now = self.get_clock().now().to_msg()
# #         path.header.stamp = now

# #         for i in range(len(waypoints)):
# #             x, y = waypoints[i]

# #             pose = PoseStamped()
# #             pose.header.frame_id = "map"
# #             pose.header.stamp = now
# #             pose.pose.position.x = x
# #             pose.pose.position.y = y

# #             if i < len(waypoints) - 1:
# #                 dx = waypoints[i + 1][0] - x
# #                 dy = waypoints[i + 1][1] - y
# #                 yaw = math.atan2(dy, dx)
# #                 q = quaternion_from_euler(0, 0, yaw)

# #                 pose.pose.orientation.x = q[0]
# #                 pose.pose.orientation.y = q[1]
# #                 pose.pose.orientation.z = q[2]
# #                 pose.pose.orientation.w = q[3]
# #             else:
# #                 pose.pose.orientation.w = 1.0

# #             path.poses.append(pose)

# #         self.path_pub.publish(path)
# #         self.get_logger().info("Published optimized path")

# #     # ========================= VISUALIZATION =========================
# #     def publish_marker(self, mask, resolution, origin_x, origin_y):
# #         marker = Marker()
# #         marker.header.frame_id = "map"
# #         marker.type = Marker.SPHERE_LIST
# #         marker.scale.x = resolution
# #         marker.scale.y = resolution
# #         marker.scale.z = resolution
# #         marker.color.g = 1.0
# #         marker.color.a = 0.8

# #         height, width = mask.shape

# #         for r in range(height):
# #             for c in range(width):
# #                 if mask[r, c]:
# #                     pt = Point()
# #                     pt.x = origin_x + c * resolution
# #                     pt.y = origin_y + r * resolution
# #                     marker.points.append(pt)

# #         self.marker_pub.publish(marker)


# # def main():
# #     rclpy.init()
# #     node = CoveragePlanner()
# #     rclpy.spin(node)
# #     node.destroy_node()
# #     rclpy.shutdown()


# # if __name__ == "__main__":
# #     main()



# # import rclpy
# # from rclpy.node import Node
# # from nav_msgs.msg import OccupancyGrid, Path
# # from rclpy.qos import QoSProfile, QoSDurabilityPolicy
# # from geometry_msgs.msg import PoseStamped
# # from tf_transformations import quaternion_from_euler

# # import numpy as np
# # import cv2
# # import math
# # import fields2cover as f2c


# # class F2CCoveragePlanner(Node):
# #     def __init__(self):
# #         super().__init__('f2c_coverage_planner')

# #         self.robot_radius = 0.225
# #         self.map_received = False
# #         qos = QoSProfile(depth=1)
# #         qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL

# #         self.create_subscription(
# #             OccupancyGrid,
# #             '/map',
# #             self.map_callback,
# #             qos
# #         )

# #         self.path_pub = self.create_publisher(Path, '/coverage_path', qos)

# #         self.get_logger().info("FULL F2C Coverage Planner Started")

# #     # ================= OCCUPANCY → F2C =================
# #     def occupancy_to_cells(self, msg):
# #         resolution = msg.info.resolution
# #         origin_x = msg.info.origin.position.x
# #         origin_y = msg.info.origin.position.y

# #         grid = np.array(msg.data).reshape(
# #             (msg.info.height, msg.info.width)
# #         )

# #         free = (grid == 0).astype(np.uint8) * 255
# #         img = 255 - free  # invert

# #         contours, hierarchy = cv2.findContours(
# #             img,
# #             cv2.RETR_CCOMP,
# #             cv2.CHAIN_APPROX_SIMPLE
# #         )

# #         if hierarchy is None:
# #             return None

# #         hierarchy = hierarchy[0]

# #         outer = None
# #         holes = []

# #         for i, contour in enumerate(contours):
# #             if hierarchy[i][3] == -1:
# #                 if outer is None or cv2.contourArea(contour) > cv2.contourArea(outer):
# #                     outer = contour
# #             else:
# #                 if cv2.contourArea(contour) > 50:
# #                     holes.append(contour)

# #         def contour_to_ring(contour):
# #             pts = []
# #             for p in contour:
# #                 col = p[0][0]
# #                 row = p[0][1]

# #                 x = origin_x + col * resolution
# #                 y = origin_y + row * resolution

# #                 pts.append(f2c.Point(x, y))

# #             pts.append(pts[0])
# #             return f2c.LinearRing(f2c.VectorPoint(pts))

# #         outer_ring = contour_to_ring(outer)

# #         cell = f2c.Cell(outer_ring)
# #         cells = f2c.Cells(cell)

# #         for hole in holes:
# #             hole_ring = contour_to_ring(hole)
# #             cells.addRing(0, hole_ring)

# #         return cells

# #     # ================= MAIN =================
# #     def map_callback(self, msg):
# #         if self.map_received:
# #             return
# #         self.map_received = True

# #         self.get_logger().info("Processing map...")

# #         cells = self.occupancy_to_cells(msg)

# #         if cells is None:
# #             self.get_logger().error("Failed to extract polygon")
# #             return

# #         # ---------------- ROBOT ----------------
# #         robot_width = self.robot_radius * 2
# #         robot = f2c.Robot(robot_width, robot_width)

# #         # ---------------- HEADLAND ----------------
# #         hl_gen = f2c.HG_Const_gen()
# #         no_hl = hl_gen.generateHeadlands(
# #             cells,
# #             3.0 * robot.getWidth()
# #         )

# #         # ---------------- OPTIMAL SWATH ANGLE ----------------
# #         bf = f2c.SG_BruteForce()

# #         best_swaths = None
# #         best_cost = float('inf')

# #         for angle in np.linspace(0, math.pi, 10):
# #             swaths = bf.generateSwaths(
# #                 angle,
# #                 robot.getCovWidth(),
# #                 no_hl
# #             )

# #             cost = swaths.getCost()

# #             if cost < best_cost:
# #                 best_cost = cost
# #                 best_swaths = swaths

# #         # ---------------- ROUTE ----------------
# #         rp = f2c.RP_RoutePlannerBase()
# #         route = rp.genRoute(no_hl, best_swaths)

# #         # ---------------- PATH (SMOOTH) ----------------
# #         pp = f2c.PP_PathPlanning()
# #         path_f2c = pp.planPath(robot, route)

# #         # ---------------- CONVERT TO ROS ----------------
# #         ros_path = Path()
# #         ros_path.header.frame_id = "map"

# #         now = self.get_clock().now().to_msg()
# #         ros_path.header.stamp = now

# #         for state in path_f2c.states:
# #             pose = PoseStamped()
# #             pose.header.frame_id = "map"
# #             pose.header.stamp = now

# #             pose.pose.position.x = state.point.getX()
# #             pose.pose.position.y = state.point.getY()

# #             yaw = state.angle
# #             q = quaternion_from_euler(0, 0, yaw)

# #             pose.pose.orientation.x = q[0]
# #             pose.pose.orientation.y = q[1]
# #             pose.pose.orientation.z = q[2]
# #             pose.pose.orientation.w = q[3]

# #             ros_path.poses.append(pose)

# #         self.path_pub.publish(ros_path)

# #         self.get_logger().info(
# #             f"Published optimal coverage path with {len(ros_path.poses)} poses"
# #         )


# # def main():
# #     rclpy.init()
# #     node = F2CCoveragePlanner()
# #     rclpy.spin(node)
# #     node.destroy_node()
# #     rclpy.shutdown()


# # if __name__ == "__main__":
# #     main()




# import rclpy
# from rclpy.node import Node
# from nav_msgs.msg import OccupancyGrid, Path
# from geometry_msgs.msg import PoseStamped
# from rclpy.qos import QoSProfile, QoSDurabilityPolicy
# from tf_transformations import quaternion_from_euler

# import numpy as np
# import cv2
# import math
# import fields2cover as f2c


# class F2CCoveragePlanner(Node):
#     def __init__(self):
#         super().__init__('f2c_coverage_planner')

#         self.robot_radius = 0.225
#         self.map_received = False

#         qos = QoSProfile(depth=1)
#         qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL

#         self.create_subscription(
#             OccupancyGrid,
#             '/map',
#             self.map_callback,
#             qos
#         )

#         self.path_pub = self.create_publisher(Path, '/coverage_path', qos)

#         self.get_logger().info("F2C v1.2.1 Coverage Planner Started")

#     # ================= OCCUPANCY → F2C =================
#     def occupancy_to_cells(self, msg):
#         resolution = msg.info.resolution
#         origin_x = msg.info.origin.position.x
#         origin_y = msg.info.origin.position.y

#         grid = np.array(msg.data).reshape(
#             (msg.info.height, msg.info.width)
#         )

#         free = (grid == 0).astype(np.uint8) * 255
#         img = 255 - free

#         contours, hierarchy = cv2.findContours(
#             img,
#             cv2.RETR_CCOMP,
#             cv2.CHAIN_APPROX_SIMPLE
#         )

#         if hierarchy is None:
#             return None

#         hierarchy = hierarchy[0]

#         outer = None
#         holes = []

#         for i, contour in enumerate(contours):
#             if hierarchy[i][3] == -1:
#                 if outer is None or cv2.contourArea(contour) > cv2.contourArea(outer):
#                     outer = contour
#             else:
#                 if cv2.contourArea(contour) > 50:
#                     holes.append(contour)

#         def contour_to_ring(contour):
#             pts = []
#             for p in contour:
#                 col = p[0][0]
#                 row = p[0][1]

#                 x = origin_x + col * resolution
#                 y = origin_y + row * resolution

#                 pts.append(f2c.Point(x, y))

#             pts.append(pts[0])
#             return f2c.LinearRing(f2c.VectorPoint(pts))

#         outer_ring = contour_to_ring(outer)

#         cell = f2c.Cell(outer_ring)
#         cells = f2c.Cells(cell)

#         for hole in holes:
#             hole_ring = contour_to_ring(hole)
#             cells.addRing(0, hole_ring)

#         return cells

#     # ================= MAIN =================
#     def map_callback(self, msg):
#         if self.map_received:
#             return
#         self.map_received = True

#         self.get_logger().info("Processing map...")

#         cells = self.occupancy_to_cells(msg)

#         if cells is None:
#             self.get_logger().error("Failed to extract polygon")
#             return

#         # ---------------- ROBOT ----------------
#         robot_width = self.robot_radius * 2
#         robot = f2c.Robot(robot_width, robot_width)

#         # ---------------- HEADLAND ----------------
#         hl_gen = f2c.HG_Const_gen()
#         no_hl = hl_gen.generateHeadlands(
#             cells,
#             3.0 * robot_width
#         )

#         # ---------------- SWATH GENERATION ----------------
#         bf = f2c.SG_BruteForce()

#         # Fixed good angle (v1.2.1 compatible)
#         angle = math.pi / 2

#         swaths = bf.generateSwaths(
#             angle,
#             robot_width,
#             no_hl
#         )

#         # ---------------- ROUTE ----------------
#         rp = f2c.RP_RoutePlannerBase()
#         route = rp.genRoute(no_hl, swaths)

#         # ---------------- PATH ----------------
#         pp = f2c.PP_PathPlanning()

#         # v1.2.1 compatibility
#         try:
#             path_f2c = pp.planPath(robot, route)
#         except:
#             path_f2c = pp.generatePath(robot, route)

#         # ---------------- CONVERT TO ROS ----------------
#         ros_path = Path()
#         ros_path.header.frame_id = "map"
#         ros_path.header.stamp = self.get_clock().now().to_msg()

#         for state in path_f2c.states:
#             pose = PoseStamped()
#             pose.header.frame_id = "map"
#             pose.header.stamp = ros_path.header.stamp

#             pose.pose.position.x = state.point.getX()
#             pose.pose.position.y = state.point.getY()

#             yaw = state.angle
#             q = quaternion_from_euler(0, 0, yaw)

#             pose.pose.orientation.x = q[0]
#             pose.pose.orientation.y = q[1]
#             pose.pose.orientation.z = q[2]
#             pose.pose.orientation.w = q[3]

#             ros_path.poses.append(pose)

#         self.path_pub.publish(ros_path)

#         self.get_logger().info(
#             f"Published coverage path with {len(ros_path.poses)} poses"
#         )


# def main():
#     rclpy.init()
#     node = F2CCoveragePlanner()
#     rclpy.spin(node)
#     node.destroy_node()
#     rclpy.shutdown()


# if __name__ == "__main__":
#     main()


import time
import rclpy
from rclpy.node import Node
import transforms3d
from geometry_msgs.msg import PoseWithCovarianceStamped


class InitAmclPosePublisher(Node):
  def __init__(self):
    super().__init__("init_amcl_pose_publisher")

    self.declare_parameter("x", value=0.0)
    self.declare_parameter("y", value=0.0)
    self.declare_parameter("theta", value=0.0)
    self.declare_parameter("cov", value=0.5**2)

    self.publisher = self.create_publisher(
        PoseWithCovarianceStamped,
        "/initialpose",
        10,
    )

    while(self.publisher.get_subscription_count() == 0):
      self.get_logger().info("Waiting for AMCL Initial Pose subscriber")
      time.sleep(1.0)

  def send_init_pose(self):
    x = self.get_parameter("x").value
    y = self.get_parameter("y").value
    theta = self.get_parameter("theta").value
    cov = self.get_parameter("cov").value

    msg = PoseWithCovarianceStamped()
    msg.header.frame_id = "map"
    msg.pose.pose.position.x = x
    msg.pose.pose.position.y = y
    quat = transforms3d.euler.euler2quat(0, 0, theta)
    msg.pose.pose.orientation.w = quat[0]
    msg.pose.pose.orientation.x = quat[1]
    msg.pose.pose.orientation.y = quat[2]
    msg.pose.pose.orientation.z = quat[3]

    msg.pose.covariance = [
        cov, 0.0, 0.0, 0.0, 0.0, 0.0,  # Pos X
        0.0, cov, 0.0, 0.0, 0.0, 0.0,  # Pos Y
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Pos Z
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Rot X
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  # Rot Y
        0.0, 0.0, 0.0, 0.0, 0.0, cov   # Rot Z
    ]

    self.publisher.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = InitAmclPosePublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

# def main(args=None):
#   rclpy.init()
#   initAmclPosePublisher = InitAmclPosePublisher()

#   future = initAmclPosePublisher.send_init_pose()

#   rclpy.spin(initAmclPosePublisher)

#   initAmclPosePublisher.destroy_node()
#   rclpy.shutdown()

if __name__ == '__main__':
    main()