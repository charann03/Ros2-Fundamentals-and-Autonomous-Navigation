#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action.client import ClientGoalHandle, GoalStatus
from rclpy.action import ActionClient
from my_robot_interfaces.action import ControlRobot
from std_msgs.msg import Empty
from rclpy.task import Future
from rclpy.executors import SingleThreadedExecutor, MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup


class ControlRobotClientNode(Node):  #Modify node_class_name heRe

    def __init__(self, executor):
        super().__init__("ControlRobotClientNode")   #Modify node_mame heRe
        self.executor = executor
        self.cb_group = ReentrantCallbackGroup()
        self.ext_publisher_cancel = False

        # action client initss
        self.control_robot_client = ActionClient(self,
                                                 ControlRobot,
                                                 "control_robot"
                                                #  ,callback_group=self.cb_group
                                                 )
        # cancel subscriber ssssss
        self.cancel_subscriber = self.create_subscription(Empty,
                                                        "cancel_topic", 
                                                        self.cancel_sub_cb,
                                                          1
                                                        #   ,callback_group=self.cb_group
                                                          )


        self.get_logger().info("control Robot action client nodess stared!!!!!!")


    def cancel_sub_cb(self, msg_ : Empty):
        if msg_:
            self.get_logger().fatal("received  a cancel request in heress")
            self.cancel_subscriber.destroy()

            self.goal_handle.cancel_goal_async().add_done_callback(self.exit_node)
        


    def exit_node(self, future: Future):
        # # print(dir(future))
        # if future.cancelled:
        #     self.get_logger().fatal("goal cancelled by an external publisher")
 
            

        #     self.executor.shutdown()
        self.ext_publisher_cancel = True



    def send_goal(self, position, velocity):
        while not self.control_robot_client.wait_for_server(1.0):    #timeout 1 sec
            self.get_logger().warn("waiting for count UntIL server......")      #warning message server

        goal = ControlRobot.Goal()
        goal.position = position
        goal.velocity = velocity

        #send goal hersss
        self.get_logger().info(" sending goal ssssss")
        self.control_robot_client.send_goal_async(goal, feedback_callback=self.fb_cb).add_done_callback(self.goal_response_callback)


    def fb_cb(self, fb_msg_ ):
        current_positions = fb_msg_.feedback.current_position
        self.get_logger().info(f"current_pos: {current_positions}")

    def goal_response_callback(self, future: Future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info("GoAL got ACCepted")
            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn("GOAl got ReJeCtEd")

    def goal_result_callback(self, future: Future):
        result : ControlRobot.Result = future.result().result
        self.get_logger().info(f"Result: {result.reached_position}")  
        self.get_logger().info(f"Result: {result.message}")     
        status = future.result().status
        #check if the goal is SuCCEEDED
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("SuCCESS")
        elif status == GoalStatus.STATUS_ACCEPTED:
            self.get_logger().info("Accepted")
        #check if the goal is ABORted
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().fatal("ABORTED")

        elif self.ext_publisher_cancel== True and status == GoalStatus.STATUS_CANCELED:
            self.get_logger().fatal("goal cancelled by an external publisher")
            # if cancel requested terminate hersss the node
            self.executor.shutdown()
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().fatal("CANcelLED")
            # if cancel requested terminate hersss the node
            # self.executor.shutdown()
        elif status == GoalStatus.STATUS_UNKNOWN:
            self.get_logger().warn("destroyed")
        
 







def main(args = None):
    rclpy.init(args= args)
    executor = SingleThreadedExecutor()
    node = ControlRobotClientNode(executor= executor)         #Modify  node_class_name heRE
    executor.add_node(node)
    node.send_goal(107,7)
    # node.send_goal(107,7)
    # node.send_goal(107,7)

    executor.spin()
    # node.send_goal(106,7)
    # rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()




