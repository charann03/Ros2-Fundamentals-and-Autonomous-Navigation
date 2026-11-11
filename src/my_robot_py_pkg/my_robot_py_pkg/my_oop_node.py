#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class MyNoDe(Node):

    def __init__(self):
        super().__init__("py_oop")
        self.counter_ = 0
        self.get_logger().info("Hellos world with oop!!!")
        self.create_timer(1.0, self.Timer_callback)

        #TimeR
    def Timer_callback(self):
        self.get_logger().info(f"Hello {self.counter_}")
        self.counter_ += 12


def main(args = None):
    rclpy.init(args= args)
    node = MyNoDe()
    rclpy.spin(node)

    rclpy.shutdown()


if __name__ == "__main__":
    main()




