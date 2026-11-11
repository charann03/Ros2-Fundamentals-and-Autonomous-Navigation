#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class Robot_subscriber(Node):  #Modify class heRe

    def __init__(self):
        super().__init__("robot_subscriber_node")   #MoDify NODE_NAME HeRe
        self.subscriber_ = self.create_subscription(String,
 "robot_pub", self.callback_robot_news, 
 10)    #(<msg_datatype>, <topic_name>, call_back_function, <Queue_size>)   

        self.get_logger().info("subscriber has started!!!")
    def callback_robot_news(self, msg_ :String):
        self.get_logger().info(msg_.data)

def main(args = None):
    rclpy.init(args= args)
    node = Robot_subscriber()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




