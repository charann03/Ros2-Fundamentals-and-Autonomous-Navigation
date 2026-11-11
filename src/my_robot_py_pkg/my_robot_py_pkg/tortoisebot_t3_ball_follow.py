#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math as m


class Ball_follow(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("ball_follow")   #Modify node_mame heRe
        #subscribe laser(lidar) data from /scan topic
        
        self.laser_subscriber = self.create_subscription(LaserScan, "/scan", self.callback_laser_dist_data, 10)
        self.velocity_publisher = self.create_publisher(Twist, "/cmd_vel" , 10)
    def callback_laser_dist_data(self, msg_:LaserScan):
        self.front_ranges = []
        for i, distance in enumerate(msg_.ranges):
            #compute angle
            #formula: angle = angle_min + (i * angle_increment)
            self.angle_ = msg_.angle_min + (i * msg_.angle_increment)
            if self.angle_> -0.261799 and self.angle_< 0.261799:
                #distance should not be nan infinity and more than 0.1metres(basic lidar dectects best past 0.1 to 0.2 metres)
                if not m.isinf(distance) and not m.isnan(distance) and distance > 0.1:
                    #append only the valid distance and the envelope angle
                    self.front_ranges.append((distance, self.angle_))
        #if no object in fov then stop!!
        self.get_logger().info("no object in fov!!!")
        mes_ = Twist()
        mes_.angular.z = 0.0
        mes_.linear.x = 0.0
        self.velocity_publisher.publish(mes_)
        # if we get distance values
        if self.front_ranges:
            #minimum angular distance tuple (distance , angle)
            min_dist_ang = min(self.front_ranges)
            #take minimum angle
            min_angle = min_dist_ang[1]
            #take minimum distance
            min_dist = min_dist_ang[0]
            #maximum angular threshold distance
            max_turn = 0.6
            #proportional constant
            k = 1.0
            #message datatype (/cmd_vel)
            #if object distance greater than 60cms 
            if min_dist> 0.6 : #minimum distance for the robot to stop from the object 0.6metres
                #if angular displacement
                if abs(min_angle) > 0.1:
                    angular = k * min_angle
                    #if min_angle is more than 0.8 then set max angular velocity to 0.8rads/s
                    mes_.angular.z = max(min(angular, max_turn), -max_turn)
                    mes_.linear.x = 0.0 
                    self.velocity_publisher.publish(mes_)
                    if min_angle>0:
                        self.get_logger().info(f"object is left!! = {min_dist}")
                    else:
                        self.get_logger().info(f"object is right!! = {min_dist}")
                #if the distance is more than 0.6metres then move only forward
                else:
                    mes_.angular.z = 0.0
                    mes_.linear.x = 0.6
                    self.velocity_publisher.publish(mes_)
                    self.get_logger().info(f"moving in front! = {min_dist}")

            #if object very near(ie.. less than 0.6) then stop if  no object then stop too!!
            else:
                mes_.angular.z = 0.0
                mes_.linear.x = 0.0 
                self.velocity_publisher.publish(mes_)
                self.get_logger().info("robot now stopping")

        # else:
        #     mes_.angular.z = 0.0
        #     mes_.linear.x = 0.0 
        #     self.velocity_publisher.publish(mes_)
        #     self.get_logger().info("robot now stopping")





def main(args = None):
    rclpy.init(args= args)
    node = Ball_follow()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




