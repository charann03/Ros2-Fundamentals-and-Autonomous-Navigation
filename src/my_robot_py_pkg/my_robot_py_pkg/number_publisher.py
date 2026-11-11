

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64

class Number_publisher(Node):  #Modify heRe

    def __init__(self):
        self.counter = 2
        super().__init__("number_publisher")   #Modify heRe
        self.get_logger().info("number_publisher node has been started!!!")
        self.publisher = self.create_publisher(Int64, "number", 10)
        self.timer = self.create_timer(1.0,self.number_callback)

    def number_callback(self):
        msg = Int64()
        msg.data = self.counter
        self.publisher.publish(msg)

def main(args = None):
    rclpy.init(args= args)
    node = Number_publisher()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
