#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedPanelState
from my_robot_interfaces.srv import SetLed
from functools import partial


class battery_node(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("battery_node")   #Modify node_mame heRe
        

        self.battery_state = "full!!"
        self.last_time_battery_state_changed = self.get_current_time_seconds()
        self.set_led_client = self.create_client(SetLed, "set_led", )
        self.battery_timer = self.create_timer(0.1,self.check_battery_state )
        self.get_logger().info("battery node has been is Started!!!")

    def get_current_time_seconds(self):
        seconds, nanoseconds = self.get_clock().now().seconds_nanoseconds()
        return seconds + nanoseconds /1000000000.0


    def check_battery_state(self):
        time_now = self.get_current_time_seconds()
        if self.battery_state == "full!!":
            if time_now - self.last_time_battery_state_changed > 4.0:
                self.battery_state = "empty!"
                self.get_logger().info("battery empty charging!!!")
                self.last_time_battery_state_changed = time_now
                self.callback_set_led_state(3, "on")

                
        elif self.battery_state == "empty!":
            if time_now - self.last_time_battery_state_changed >6:
                self.battery_state = "full!!"
                self.get_logger().info("battery is now full!!")
                self.last_time_battery_state_changed = time_now
                self.callback_set_led_state(3, "off")



    def callback_set_led_state(self, led_number, led_state):
        while not self.set_led_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("waiting for set_led service!!!")

        request = SetLed.Request()
        request.lednumber = led_number
        request.state = led_state

        future = self.set_led_client.call_async(request)
        future.add_done_callback(partial(self.callback_call_set_led, request=request))

    def callback_call_set_led(self, future, request):
        response : SetLed.Response = future.result()
        if response.success:
            self.get_logger().info("LED turnED On!!!!")
        else: self.get_logger().info("LED STATE NOTCHANGED!!!")








def main(args = None):
    rclpy.init(args= args)
    node = battery_node()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




