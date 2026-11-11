#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class Number_counter(Node):  #Modify heRe

    def __init__(self):
        self.sum = 0
        super().__init__("number_counter")   #Modify heRe
        self.get_logger().info("number counter node has been started")
        self.subscriber = self.create_subscription(Int64, "/number",self.number_receive , 10)
        self.publisher = self.create_publisher(Int64, "number_count", 10)
        self.reset_sum_server = self.create_service(SetBool, "reset_counter" ,self.Callback_reset_counter )
        self.timer = self.create_timer(1.0, self.number_count_callback)

    def number_receive(self, msg:Int64):
        self.sum += msg.data

    def number_count_callback(self):
        msg_ = Int64()
        msg_.data = self.sum
        self.publisher.publish(msg_)


    def Callback_reset_counter(self,request: SetBool.Request, response: SetBool.Response):
        if request.data == True:
            self.sum = 0
            response.success = True
            response.message = "counter is reset!!!"

        else:
            response.success  = False
            response.message = "counter is notReSeT!!!"
        return response   #always return the response for the service is mandatory!!!


def main(args = None):
    rclpy.init(args= args)
    node = Number_counter()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()