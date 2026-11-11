#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts


def main(args = None):
    rclpy.init(args= args)
    node = Node("add_two_ints_client_no_oop")         #Modify  node_class_name heRE
    #create the service client in heress
    client = node.create_client(AddTwoInts, 
                                "add_two_ints")
    while not client.wait_for_service(1.0): # wait untill the server becomes active
        node.get_logger().warn("waiting for add_two_ints server")
    # update the service parameters in heress    
    request = AddTwoInts.Request()
    request.a = 6
    request.b = 6
    #returns the future object
    future = client.call_async(request=request)
    #spin the node until we receive the response
    rclpy.spin_until_future_complete(node=node,       #node object
                                     future=future,   #future object from service client
                                     executor=None,    # defaults to global executor
                                     timeout_sec=None)  # timeout to spin till future

    response = future.result() # returns the sum
    #print the output
    node.get_logger().info(f"{request.a} + {request.b} = {response.sum}")





    
    # rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




