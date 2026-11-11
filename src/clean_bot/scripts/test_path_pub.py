#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Path
from geometry_msgs.msg import PoseStamped


class Test_Path_Node(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("Test_Path_Node")   #Modify node_mame heRe
        self.path_pub = self.create_publisher(Path, "/test_path" , 10)
        self.path_coords = [
    (-0.04303000122308731, 0.1590770035982132),
    (2.2197110652923584, 0.03638499975204468),
    (2.285006046295166, 3.730086088180542),
    (-0.09555000066757202, 3.695594072341919),
    (2.381866931915283, 6.540656089782715),
    (-0.260233998298645, 6.532648086547852)
                           ]
        self.latest_path = None
        self.pub_timer = self.create_timer(0.1, self.publish_continuous_path)


    def publish_continuous_path(self):
        if self.latest_path is not None:
            # self.latest_path.header.stamp = self.get_clock().now().to_msg()
            self.path_pub.publish(self.latest_path)
            # print("Re-published latest path")
        

    def path_publish(self):
        path = Path()
        path.header.frame_id = "map"
        path.header.stamp = self.get_clock().now().to_msg()
        for p in self.path_coords:
            point = PoseStamped()
            point.header.frame_id = "map"
            point.header.stamp = self.get_clock().now().to_msg()
            point.pose.position.x = p[0]
            point.pose.position.y = p[1]
            point.pose.position.z = 0.0
            point.pose.orientation.w = 1.0
            point.pose.orientation.x = 0.0
            point.pose.orientation.y = 0.0
            point.pose.orientation.z = 0.0
            path.poses.append(point)
        self.latest_path = path
        self.path_pub.publish(path)




def main(args = None):
    rclpy.init(args= args)
    node = Test_Path_Node()         #Modify  node_class_name heRE
    node.path_publish()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




