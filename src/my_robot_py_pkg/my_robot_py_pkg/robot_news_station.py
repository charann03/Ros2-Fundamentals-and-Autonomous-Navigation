

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import String


class robotnewsstation(Node):

    def __init__(self):
        # self.robot_name = "arthur"
        super().__init__("robot_news_station")  #Modify node_mame heRe
        self.rob_pub = self.create_publisher(String, "robot_news", 10)
        self.declare_parameter("robot_name", "arthur")
        self.robot_name = self.get_parameter("robot_name").value
        self.get_logger().info("robot news station has been started!!!!!!")
        self.timer = self.create_timer(1, self.message_callback)



    def message_callback(self):
        msg_ = String()
        msg_.data = f"my name is : {self.robot_name}"
        self.rob_pub.publish(msg_)



def main(args = None):
    rclpy.init(args= args)
    node = robotnewsstation()        #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




