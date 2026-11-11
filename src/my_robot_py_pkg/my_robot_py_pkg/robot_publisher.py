#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String    # String message types 



class Robot_publish(Node):  #Modify heRe

    def __init__(self):
        # self.counter = 0
        super().__init__("robot_publisher_node")   #Modify <Node_naME> heRe
        self.get_logger().info("Publisher has started with the ros2")
        self.declare_parameter("counter", 1)
        self.counter = self.get_parameter("counter").value
        self.publisher_ = self.create_publisher(String, "robot_pub", 10)   #(<Msg_datatype>, <topic_name>, <Queue_size>)
        self.timer = self.create_timer(1, self.publish_news)

    def publish_news(self):
        # self.counter +=1
        msg_ = String()
        msg_.data = f"message is moving {self.counter} times!!!"
       #self.get_logger().info(f"message is moving {self.counter} times!!!")
        self.publisher_.publish(msg_)

def main(args = None):
    rclpy.init(args= args)
    node = Robot_publish()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




