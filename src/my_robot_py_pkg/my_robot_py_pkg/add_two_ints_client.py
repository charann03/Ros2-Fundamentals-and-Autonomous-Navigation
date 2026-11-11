#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial

class add_two_ints_client_node(Node):  #Modify heRe

    def __init__(self):
        super().__init__("add_two_ints_client_node")   #Modify heRe
        self.client = self.create_client(AddTwoInts,
         "add_two_ints")      #(DATATYpe , <service_nAME>)

    def call_add_two_ints(self, a, b):
        # check for service_server
        while not self.client.wait_for_service(1.0):    #timeout 1 sec
            self.get_logger().warn("waiting for add two ints server......")      #warning message server
        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client.call_async(request) # send the request
        # when the client receives the response call the callback function
        # to get request params use partial() function it is similar to std::bind in cpp
        future.add_done_callback(partial(self.callback_call_add_two_ints, request=request))




    def callback_call_add_two_ints(self, future, request):
        response = future.result()
        self.get_logger().info(f"got response: {request.a} + {request.b} = {response.sum}")


def main(args = None):
    rclpy.init(args= args)
    node = add_two_ints_client_node()       #Modify heRE
    node.call_add_two_ints(16,389)
    node.call_add_two_ints(3,6)
    node.call_add_two_ints(12,24)

    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




