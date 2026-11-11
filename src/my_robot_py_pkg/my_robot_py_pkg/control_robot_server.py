#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action.server import ActionServer, CancelResponse, GoalResponse, GoalInfo, ServerGoalHandle
from my_robot_interfaces.action import ControlRobot
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from time import sleep
from threading import Lock


class ControlRobotServerNode(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("ControlRobotServerNode")   #Modify node_mame heRe
        # satrting position heress
        self.starting_position = 50
        # thread lock for preempting !!! !!!
        self.goal_lock_ = Lock()
        # preempted goal is
        self.preempt_goal_id : GoalInfo.goal_id = None
        self.goal_handle_ : ServerGoalHandle = None
        # cancel new goals
        self.goal_active_ = False


        self.control_robot_server_ = ActionServer(self,
                                                  ControlRobot,
                                                  "control_robot",
                                                  execute_callback=self.execute_callback,
                                                  goal_callback= self.goal_callback,
                                                  cancel_callback= self.cancel_callback,
                                                  handle_accepted_callback= self.handle_accepted_callback,
                                                  callback_group=ReentrantCallbackGroup())
        self.get_logger().info("ACTion server has been is STArTED!!!!!!") 


    def goal_callback(self, goal_request: ControlRobot.Goal):
        self.get_logger().info("received a goal!!!!!!")
        if goal_request.position <= 0 or goal_request.velocity <= 0:
            self.get_logger().warn( "position or velocity cant be a negative or zero, rejectiong goal!!!!!!")
            return GoalResponse.REJECT

        # reject new goalss and proceed with old in heress
        # with self.goal_lock_:

        #     if self.goal_active_:
        #             self.get_logger().info("old goal is active rejecting new goalss!!!!!!")
        #             return GoalResponse.REJECT

        # else accept the goal
        self.goal_active_ = True
        self.get_logger().info("goal accepted heresss")
        return GoalResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle: ServerGoalHandle):
        # preempt goal with goal id
        with self.goal_lock_:
            if self.goal_handle_ and self.goal_handle_.is_active:
                self.preempt_goal_id = self.goal_handle_.goal_id
                self.get_logger().info(f"Aborting current goal and ACCEPTING New GoalSS!!!!!! preempted goal id: {self.preempt_goal_id}")
                self.goal_handle_.abort()
            # store new goal_handle
            self.goal_handle_ = goal_handle




        goal_handle.execute() 




    def execute_callback(self, goal_handle: ServerGoalHandle):
        # # goal_lock for goal handle preemption
        # with self.goal_lock_:
        #     self.goal_handle_ = goal_handle

        #Get request from the is goal!!
        position = goal_handle.request.position
        velocity = goal_handle.request.velocity
        # feedback ins heress
        feedback = ControlRobot.Feedback()
        # result
        result = ControlRobot.Result()

        # action working heress
        current_position = self.starting_position

        while current_position < position:

            # for cancelling heress
            if goal_handle.is_cancel_requested:
                if current_position == position:
                    self.get_logger().warn("cancel requested but goal is reached")
                    result.reached_position = current_position
                    result.message = "goal reached cant cancel in heress"
                    goal_handle.succeed()
                    
                    return result
                else:
                    self.get_logger().warn("cancel requested, cancelling the goalss heress")
                    result.reached_position = current_position
                    result.message = "cancel requested, cancelling the goalss heress"
                    goal_handle.canceled()
                    return result
            # preempt goal with goal id hersss
            # elif self.preempt_goal:
            # elif goal_handle.goal_id == self.preempt_goal_id:
            #     with self.goal_lock_:
            
            #         self.get_logger().warn("new goal received aborting old goalss!!!!!!")
            #         result.reached_position = current_position
            #         result.message = "goal reached cant cancel in heress"
            #         goal_handle.abort()
            #         return result
            elif not goal_handle.is_active:
                self.get_logger().warn(
                    "Goal was preempted. Stopping execution."
                )

                result.reached_position = current_position
                result.message = "Goal preempted"

                return result
                    


            # move the robot
            elif (position - current_position) < velocity:
                current_position += (position - current_position)

            else:
                current_position += velocity
            ## publ#ish feedss backss
            feedback.current_position = current_position
            goal_handle.publish_feedback(feedback=feedback)
            self.get_logger().info(f"current_position of robots is: {current_position}")
            sleep(1.0) # to mimic m/s


        # return result
        if current_position == position:
            self.get_logger().info("goal is reached !!!!!! !!!!!! !!!!!!")
            result.reached_position = current_position
            result.message = "goal reached in hersss is heress"
            goal_handle.succeed()
            # accept the new goal since old goal is completed
            self.goal_active_ = False

            return result

        else:
            self.get_logger().warn("goal not reached, aborting in heress!!!!!!")
            result.reached_position = current_position
            result.message = "goal reached cant cancel in heress"
            goal_handle.abort()
            self.goal_active_ = False
            # accept the new goal since old goal is completed
            return result





    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("received a cancel request in heress!!!!!!")
        return CancelResponse.ACCEPT


    



def main(args = None):
    rclpy.init(args= args)
    node = ControlRobotServerNode()         #Modify  node_class_name heRE
    executor = MultiThreadedExecutor()
    executor.add_node(node=node)
    executor.spin()
    # rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()