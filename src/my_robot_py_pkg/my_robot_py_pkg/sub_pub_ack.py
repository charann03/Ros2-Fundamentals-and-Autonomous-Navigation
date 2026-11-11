#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class MyNoDe(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("py_oop")   #Modify node_mame heRe
        self.subscriber = self.create_subscription(
                                                    String,
                                                    "/chatter",
                                                    self.callback,
                                                    10
        )
        self.timer_ = self.create_timer(2.0, self.check_pub)
        self.msg_received = False

    def callback(self, msg_):
        self.get_logger().info(f"{msg_.data}")
        self.msg_received = True

    def check_pub(self):
        if not self.msg_received:
            self.get_logger().info("msg not receuveddd")
        else:
            # self.get_logger().info("msg receuveddd w")
            self.msg_received = False

            




    



def main(args = None):
    rclpy.init(args= args)
    node = MyNoDe()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




