#! /usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Float32
from sensor_msgs.msg import LaserScan
import math as m



class Laser_dist(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("laser_dist")   #Modify node_mame heRe
        #subscribe laser(lidar) data from /scan topic
        self.laser_subscriber = self.create_subscription(LaserScan, "/scan", self.callback_laser_dist_data, 10)
        #publish closest distance values
        self.dist_publisher = self.create_publisher(Float32, "closest_object_distance", 10)





    def callback_laser_dist_data(self, msg_:LaserScan):
        self.front_ranges = []
        for i, distance in enumerate(msg_.ranges):
            #compute angle
            #formula: angle = angle_min + (i * angle_increment)
            self.angle_ = msg_.angle_min + (i * msg_.angle_increment)
            if self.angle_> -0.261799 and self.angle_< 0.261799:
                #distance should not be nan infinity and more than 0.1metres(basic lidar dectects best past 0.1 to 0.2 metres)
                if not m.isinf(distance) and not m.isnan(distance) and distance > 0.1:
                    #append only the valid distance
                    self.front_ranges.append(distance)
        # if we get distance values
        if len(self.front_ranges) > 0:
            #most closest object = min distance from lidar to object
            self.closest_dist_ = min(self.front_ranges)
            # if hasattr(self, "closest_dist_"):
            #publish closest distance data
            mes_ = Float32()
            mes_.data = self.closest_dist_
            self.dist_publisher.publish(mes_)
        # if we do not get distance values ie.. empty space
        else :
            #just publish infinity
            mes_ = Float32()
            mes_.data = float("inf")
            self.dist_publisher.publish(mes_)
            self.get_logger().info("no object nearby!!!!!!")


    # def publish_closest_dist(self):
    #     if hasattr(self, "closest_dist_"):
    #         mes_ = Float32()
    #         mes_.data = self.closest_dist_
    #         self.dist_publisher.publish(mes_)



def main(args = None):
    rclpy.init(args= args)
    node = Laser_dist()         #Modify  node_class_name heRE
    # node.create_timer(1, node.publish_closest_dist)

    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

