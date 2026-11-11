#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import HardwareStatus   #msg not recognised? then reopen vs_code from terminal after sourcing the terminal
from my_robot_interfaces.srv import ComputeRectangleArea


class Hardware_status_publisher_node(Node):  #Modify heRe

    def __init__(self):
        super().__init__("hardware_status_publisher")   #Modify heRe
        self.hw_status_pub = self.create_publisher(HardwareStatus, "Hardware_status", 10)
        self.timer = self.create_timer(1.0, self.publish_hw_status)
        self.area_comp_service = self.create_service(ComputeRectangleArea, "compute_rect_area", self.callback_rect_area)
        self.get_logger().info("the state publisher has been started!!!")


    def publish_hw_status(self):
        msg = HardwareStatus()
        msg.temperature = 36.6
        msg.are_motors_ready = True
        msg.debug_message = "A custom msg"
        self.hw_status_pub.publish(msg)

    def callback_rect_area(self, request: ComputeRectangleArea.Request, response: ComputeRectangleArea.Response):
        response.area = request.length * request.width
        self.get_logger().info(f"area is = {response.area}")
        return response

def main(args = None):
    rclpy.init(args= args)
    node = Hardware_status_publisher_node()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




