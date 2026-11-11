

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from rclpy.parameter import Parameter
from rcl_interfaces.msg import SetParametersResult

class Number_publisher(Node):  #Modify heRe

    def __init__(self):
        # self.counter = 2
        super().__init__("number_publisher")   #Modify heRe
        self.declare_parameter("number", 2)   #("<parameter_name!>" , 2 = value (datatype= INT)) ie.. "number" parameter takes integer values
        self.declare_parameter("time_period" , 1.0) #("<parameter_name!>", 1.0 = datatype= FLOAT)  "time_period" paramter takes float value  
        self.number_ = self.get_parameter("number").value   #(<parameter_value> ,).value --> no ()
        self.time_period_ = self.get_parameter("time_period").value
        self.add_on_set_parameters_callback(self.params_callback)


        self.get_logger().info("number_publisher node has been started!!!")
        self.publisher = self.create_publisher(Int64, "number_top", 10)
        self.timer = self.create_timer(self.time_period_,self.number_callback)

    def number_callback(self):
        msg = Int64()
        msg.data = self.number_
        self.publisher.publish(msg)


    def params_callback(self, params: list[Parameter]):
        result = SetParametersResult()
        for param in params:
            if param.name == "number":
                self.number_ = param.value
                result.successful = True
            if param.name == "time_period":
                self.time_period_ = param.value
                self.timer.cancel()
                if self.timer.is_canceled():
                    self.timer = self.create_timer(self.time_period_, self.number_callback)
                    result.successful = True
        return result
        
def main(args = None):
    rclpy.init(args= args)
    node = Number_publisher()         #Modify heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()
