#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action.client import ClientGoalHandle, GoalStatus
from rclpy.action import ActionClient
from my_robot_interfaces.action import CountUntil
from rclpy.task import Future
from rclpy.executors import SingleThreadedExecutor, MultiThreadedExecutor
import threading
import time

class CountUntilClient_Node(Node):  #Modify node_class_name heRe

    def __init__(self, executor):
        super().__init__("count_until_client")   #Modify node_mame heRe
        self.count_until_client_ = ActionClient(self, CountUntil, "count_until")
        # print(Node.default_callback_group()) // default is mutually exclusive callback group
        # executor reference variable
        self.executor = executor



    def send_goal(self, target_number, period):
        # wait!! for the server
        #self.count_until_client_.wait_for_server()       ##this leads the client to wait for server continuously(infinite)
        while not self.count_until_client_.wait_for_server(1.0):    #timeout 1 sec
            self.get_logger().warn("waiting for count UntIL server......")      #warning message server


        # create a goal!!
        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period

        # SEND!! the GOal
        self.get_logger().info("sending goal!!")
        self.count_until_client_.send_goal_async(goal  # future = action_client.send_goal_async()
        #hear the feedback from the server
        ,feedback_callback=self.goal_feedback_callback      
        #check whether the goal is accepted or not                                 
        ).add_done_callback(self.goal_response_callback) #for result -> future.add_done_callback(callback_function)     #never use send_goal function use send_goal_async function always
        #CANCEL A GOAL
        #send a cancel request 3 seconds later
        # self.timer_ = self.create_timer(3.0,self.cancel_goal)

    def cancel_goal(self):
        self.get_logger().info("Send A Cancel requeSt")
        #Cancel the goaLSS
        self.goal_handle.cancel_goal_async()
        self.timer_.cancel() # this prevents the timer to run only once instead of running endlessly for every 3 seconds


    #feedback callback function
    def goal_feedback_callback(self, feedback_msg):
        number = feedback_msg.feedback.current_number  #refering the current_number inside the feedback of the countuntil action
        #just print LOG the curent_number as the feedback
        self.get_logger().info("GGOTtt feedback: " + str(number))
        # you can cancel the goal through the feedback ttoooo
        
    def goal_response_callback(self, future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info("GoAL got ACCepted")
            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn("GOAl got ReJeCtEd")
            # self.destroy_node() # destroy all action client associated with this code
            # rclpy.shutdown() # shutdown if rejected
            # self.executor.shutdown() #shutdown the node here immediately


    def goal_result_callback(self, future):
        result = future.result().result     # THIS!! future.result().result --> this .result refers to the action result that we denoted in our action file!!
        status = future.result().status
        #check if the goal is SuCCEEDED
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("SuCCESS")
        elif status == GoalStatus.STATUS_ACCEPTED:
            self.get_logger().info("Accepted")
        #check if the goal is ABORted
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().fatal("ABORTED")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().error("CANcelLED")
        elif status == GoalStatus.STATUS_UNKNOWN:
            self.get_logger().info("destroyed")
        self.get_logger().info(f"Result: {result.reached_number}")      # reached_number is under Result in action_file(CountUntil.action)!!!!!!


def main(args = None):
    rclpy.init(args= args)
    executor = SingleThreadedExecutor()
    node = CountUntilClient_Node(executor=executor)         #Modify  node_class_name heRE
    executor.add_node(node)
    node.send_goal(6, 1.2)
    # time.sleep(1)
    node.send_goal(12, 0.5)
    # node.send_goal(6, 1.2)
    # # time.sleep(1)
    # node.send_goal(12, 0.5)

    executor.spin()
    # rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()




