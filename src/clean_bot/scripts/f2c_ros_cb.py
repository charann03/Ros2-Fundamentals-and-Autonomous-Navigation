#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, QoSDurabilityPolicy
from nav_msgs.msg import OccupancyGrid
import numpy as np
import matplotlib.pyplot as plt
import cv2
from scipy.ndimage import binary_dilation, label
import fields2cover as f2c
import math
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped
from tf_transformations import quaternion_from_euler



class zigzag_path_planner(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("path_planner_node")   #Modify node_mame heRe
        self.map_received = False
        qos = QoSProfile(depth=1)
        qos.durability = QoSDurabilityPolicy.TRANSIENT_LOCAL
        self.subscription = self.create_subscription(OccupancyGrid, '/map', self.map_callback, qos)
        self.path_pub = self.create_publisher(Path , "/coverage_path", 10)
        self.latest_path = None
        self.timer = self.create_timer(0.5, self.publish_continuous_path)

    def publish_continuous_path(self):
        if self.latest_path is not None:
            self.path_pub.publish(self.latest_path)


    def map_callback(self, msg):
        if self.map_received:
            return
        self.map_received = True
        self.get_logger().info("Map received!")

        grid = np.array(msg.data).reshape((msg.info.height, msg.info.width))

        res = msg.info.resolution
        origin_x = msg.info.origin.position.y
        origin_y = msg.info.origin.position.x
        self.map_height = msg.info.height
        self.map_resolution = msg.info.resolution
        self.origin_x = msg.info.origin.position.x
        self.origin_y = msg.info.origin.position.y
        self.width = msg.info.width

        height, width = grid.shape
        self.get_logger().info(f"Map size: {width}x{height}, resolution: {res:.3f}")

        free_mask = grid == 0
        print(free_mask)
        obstacle_mask = grid == 100

        dilated_obstacles = binary_dilation(obstacle_mask, iterations=10, border_value=1)
        nav_mask = np.logical_and(free_mask, ~dilated_obstacles)

        labeled, _ = label(nav_mask)
        start_x_px = int(-origin_x / res) #int(-(-0.9/0.05)) = 18

        start_y_px = int(-origin_y / res) # int(-(-0.7/0.05)) = 13

        start_x_px = np.clip(start_x_px, 0, height - 1)
        start_y_px = np.clip(start_y_px, 0, width - 1)
        # to find the robot region so that path need not to be planned accross that region
        robot_region = labeled[start_x_px, start_y_px]


        # Create RGB image
        overlay = np.zeros((height, width, 3), dtype=np.uint8)

        #  Navigable area
        overlay[nav_mask] = [0, 255, 0] #green

        #  Dilated obstacles
        overlay[dilated_obstacles] = [255, 0, 0]

        #  Original obstacles (override for visibility)
        overlay[obstacle_mask] = [0, 0, 0]

        # Plot
        plt.figure(figsize=(6,6))
        plt.imshow(overlay)

        # 🔵 Robot position
        plt.scatter(start_y_px, start_x_px, c='blue', s=60, label='Robot')

        plt.title("Navigation Map Overlay")
        plt.xlabel("X")
        plt.ylabel("Y")

        plt.legend()
        plt.axis('equal')
        plt.grid(False)

        plt.ion()
        plt.show(block=False)
        # convert into a binary image
        robot_mask = (labeled == robot_region).astype(np.uint8) * 255
        #smooth the edges
        kernel = np.ones((3,3), np.uint8)
        robot_mask = cv2.morphologyEx(robot_mask, cv2.MORPH_CLOSE, kernel)
        contours, hierarchy = cv2.findContours(
            robot_mask,
            cv2.RETR_CCOMP,   # gives outer + holes
            cv2.CHAIN_APPROX_SIMPLE
        )

        outer_polygons = []
        inner_polygons = []
        # print(contours)

        for i, cnt in enumerate(contours):
            epsilon = 0.01 * cv2.arcLength(cnt, True) #degree of closeness to the actual perimeter of the contour
            approx = cv2.approxPolyDP(cnt, epsilon, True) # removes unnecessary pts and preserves the originl shape
            print(approx.shape)
            pts = approx.squeeze() #reduces one extra dimension  ie.. from approx -> (8, 1, 2)(no of contours, extra dimension, (x,y)coords_length ie 2)

            print(pts.shape)
            if len(pts.shape) != 2:   #to remove noise
                continue

            world_pts = []
            for p in pts:
                x = origin_x + p[1] * res   #  NOTE: column → x
                y = origin_y + p[0] * res   #  row → y

                world_pts.append((x, y))

            # ensure closed polygon
            if world_pts[0] != world_pts[-1]:
                world_pts.append(world_pts[0])

            # classify
            if hierarchy[0][i][3] == -1:
                outer_polygons.append(world_pts)

            else:
                inner_polygons.append(world_pts)

        plt.figure(figsize=(6, 6))

        # 🔵 Plot outer boundary
        for poly in outer_polygons:
            xs = [p[0] for p in poly] + [poly[0][0]]  # close loop
            ys = [p[1] for p in poly] + [poly[0][1]]
            plt.plot(xs, ys, 'b-', linewidth=2, label='Outer' if 'Outer' not in plt.gca().get_legend_handles_labels()[1] else "")

        # original obstacles
        for obs in inner_polygons:
            xs = [p[0] for p in obs] + [obs[0][0]]
            ys = [p[1] for p in obs] + [obs[0][1]]
            plt.plot(xs, ys, 'r--', label='Original')


        plt.title("Vector Map (Polygons)")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.axis('equal')
        plt.grid(True)
        # plt.legend()
        plt.show(block=False)
        plt.pause(0.5)
                  #f2c


        # OUTER

        outer_pts = [f2c.Point(x, y) for x, y in outer_polygons[0]]
        # print(f"outer points is: {outer_pts}")
        ring = f2c.LinearRing(f2c.VectorPoint(outer_pts))
        outer_ring = f2c.Cells(f2c.Cell(ring))
        # print(ring.isClosed())


        # # # INNER (holes)

        for obs in inner_polygons:
            obs_pts = [f2c.Point(x, y) for x, y in obs]
            outer_ring.addRing(0, f2c.LinearRing(f2c.VectorPoint(obs_pts)))

            ### Path Planning ###
        robot_c = f2c.Robot(0.5) # param1 - robot width
        const_hl = f2c.HG_Const_gen()
        mid_hl_c = const_hl.generateHeadlands(outer_ring, 1 * robot_c.getWidth())
        bf = f2c.SG_BruteForce()
        swaths_c = bf.generateSwaths(-math.pi/2, robot_c.getCovWidth(), mid_hl_c)
        #route planner
        route_planner = f2c.RP_RoutePlannerBase()
        route = route_planner.genRoute(mid_hl_c, swaths_c)
        robot_c.setMinTurningRadius(0.0)  # m robot min turning radius
        robot_c.setMaxDiffCurv(0.1);  # 1/m^2 robot maxdiffcurv
        path_planner = f2c.PP_PathPlanning()
        #dubins curves
        dubins = f2c.PP_DubinsCurves()
        path_dubins = path_planner.planPath(robot_c, route, dubins);
        # print(path_dubins.getStates())
        self.publish_f2c_path(path_dubins)
        




        f2c.Visualizer.figure()
        f2c.Visualizer.plot(outer_ring)
        f2c.Visualizer.plot(mid_hl_c)
        f2c.Visualizer.plot(path_dubins)

    def extract_corners(self,points):
        if len(points) < 2:
            return points
    
        corners = []
    
        # always keep first point
        corners.append(points[0])
    
        for i in range(1, len(points)-1):
            prev_angle = round(points[i-1][2], 2)
            curr_angle = round(points[i][2], 2)
    
            if curr_angle != prev_angle:
                corners.append(points[i])
    
        # always keep last point
        corners.append(points[-1])
    
        return corners


    def publish_f2c_path(self, path_dubins):

        states = path_dubins.getStates()

        if not states:
            self.get_logger().warn("Empty F2C path")
            return
        

        now = self.get_clock().now().to_msg()

        path_msg = Path()
        path_msg.header.frame_id = "map"
        path_msg.header.stamp = now

        all_points = []
 
        for state in states:
            x = state.point.getX()
            y = state.point.getY()
            theta = round(state.angle, 2)
        
            all_points.append((x, y, theta))

        corner_points = self.extract_corners(all_points)
        print(f"Corner points:{corner_points}")

        for point in corner_points:
            x, y, theta = point
            pose = PoseStamped()
            pose.header.frame_id = "map"
            pose.header.stamp = now

            x_rot = y
            y_rot = -x
            x =  x_rot
            y =  y_rot 
            
            # mirror
            y = -y
            pose.pose.position.x = x 
            pose.pose.position.y = y 
            pose.pose.position.z = 0.0

            q = quaternion_from_euler(0, 0, theta)
            pose.pose.orientation.x = q[0]
            pose.pose.orientation.y = q[1]
            pose.pose.orientation.z = q[2]
            pose.pose.orientation.w = q[3]

            path_msg.poses.append(pose)

        self.latest_path = path_msg
        self.path_pub.publish(path_msg)
        self.get_logger().info(f"Published F2C Path with {len(path_msg.poses)} poses")



def main(args = None):
    rclpy.init(args= args)
    node = zigzag_path_planner()         #Modify  node_class_name heRE
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        plt.close('all')
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()




