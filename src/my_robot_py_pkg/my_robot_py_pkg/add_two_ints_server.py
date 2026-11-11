#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class add_two_ints_server_NodE(Node):  #Modify class_NAMe heRe

    def __init__(self):
        super().__init__("add_two_ints_server_node")   #Modify heRe
        self.server = self.create_service(AddTwoInts, "add_two_ints", 
        self.callback_add_two_INTs) #(DATatype, <service_name>, callback_function)
        self.get_logger().info("add two ints server has been started!!!")



    def callback_add_two_INTs(self, request: AddTwoInts.Request, Response: AddTwoInts.Response):
        Response.sum = request.a + request.b
        self.get_logger().info(f"{request.a} + {request.b} = {Response.sum}")
        return Response #MUST RETURN THE RESPONSE


def main(args = None):
    rclpy.init(args= args)
    node = add_two_ints_server_NodE()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

# to checkss the server node runnin
"""ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 3 , b: 6}"
"""


