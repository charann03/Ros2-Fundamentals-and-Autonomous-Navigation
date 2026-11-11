#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LedPanelState
from my_robot_interfaces.srv import SetLed



class Led_panel_node(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("Led_panel_node")   #Modify node_mame heRe
        # self.led_states = [0, 0, 0]
        self.declare_parameter("led_number1", 0)
        self.declare_parameter("led_number2", 0)
        self.declare_parameter("led_number3", 0)
        self.led_number1 = self.get_parameter("led_number1").value
        self.led_number2 = self.get_parameter("led_number2").value
        self.led_number3 = self.get_parameter("led_number3").value
        self.led_states = [self.led_number1, self.led_number2, self.led_number3]
        self.led_pnl_state_pub = self.create_publisher(LedPanelState, 
        "led_panel_state", 10)
        self.set_led_server = self.create_service(SetLed, "set_led", self.callback_set_led_server)
        self.timer = self.create_timer(5.0, self.callback_led_pnl_state_pub)
        self.get_logger().info("led_panel node started!!!!!!")


    def callback_led_pnl_state_pub(self):
        msg = LedPanelState()
        msg.ledstate = self.led_states
        self.led_pnl_state_pub.publish(msg)


    def callback_set_led_server(self, request: SetLed.Request, response: SetLed.Response):
        led_number = request.lednumber
        state = request.state

        if led_number >= len(self.led_states) | led_number <= 0:
            response.success = False
            return response
        

        if state not in ["off", "on"]:
            response.success = False
            return response
        
        if state == "on":
            self.led_states[led_number-1] = 1
            return response

        if state == "off":
            self.led_states[led_number-1] = 0
            return response



def main(args = None):
    rclpy.init(args= args)
    node = Led_panel_node()         #Modify  node_class_name heRE
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




