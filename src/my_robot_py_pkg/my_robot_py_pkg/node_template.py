#!/usr/bin/env python3
import rclpy
from rclpy.node import Node


class MyNoDe(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("py_oop")   #Modify node_mame heRe


def main(args = None):
    rclpy.init(args= args)
    node = MyNoDe()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




