#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
import threading
#imports necessary for action
#from rclpy.action import ActionServer
#from my_robot_interfaces.action import CountUntil
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle, GoalEvent
from my_robot_interfaces.action import CountUntil
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup


class CountUntilServer_Node(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("Count_until_server")   #Modify node_mame heRe
        #to make sure the first goal does'nt get rejected 
        self.goal_handle_: ServerGoalHandle = None
        #preventing same variable utilized by two threads ie.. self.goal_handle_
        self.goal_lock  = threading.Lock()
        #goal queue
        self.goal_queue_ = []
        # create goal event object
        # set external goal_active to prevent race condition
        self.goal_active_ = False
        self.count_until_server_ = ActionServer(self, 
                                    CountUntil, 
                                    "count_until", # name of the action server
                                    #accecpt the goal or not
                                    goal_callback= self.goal_callback, # default without a goal callback any goal is directly accepted(if given this callback runs first before the execute callback)
                                    #execute the goal (compulsory for a basic action server)
                                    execute_callback=self.execute_callback,
                                    #cancel the goal or not
                                    cancel_callback=self.cancel_callback,
                                    #enable mutithreading for cancel the goal
                                    callback_group=ReentrantCallbackGroup(),
                                    #Queue goals handle multiple goals callback
                                    handle_accepted_callback= self.handle_accepted_callback )      # self.count_until_server_ = ActionServer(self, <action_data__file>, "<action_NaME", execute_callback=self.<callback_function_that_we_define_into>)
                                    
        self.get_logger().info("ACTion server has been is STArTED!!!!!!") 

    def goal_callback(self, goal_request: CountUntil.Goal):
        self.get_logger().info("Receieved a goal!!")
        #policy : refuse newgoal if current goal is active
        #--------------------------------------------------------
        # with self.goal_lock: # this enables the goal handle attribute to be used by only one callbak functisn
        #     # if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #     if self.goal_active_: # so thst the first goal never gets rejected
        #         self.get_logger().info("a goalll already active rejecting new goalss")
        #         return GoalResponse.REJECT
        #     # after first goal make it active
        #     self.goal_active_ = True
            
        #--------------------------------------------------------

        #validate the goal requestsss
        if goal_request.target_number <= 0: # accept only target number is positive
            self.get_logger().warn("rejecting the goal!!, only positive Integers as target_number")
            return GoalResponse.REJECT
        
        # #policy : preempt(terminate) exixting goal when receiving new goal
        # NOTE: (dont uncomment this working case is in handle accepted callback)
        # #---------------------------------------------------------
        # with self.goal_lock:
        #     # if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #     if self.goal_handle_ is not None and self.goal_active_:
        #         self.get_logger().info("abort current goal and ACCEPTING THR NEW GOAL!!") 
        #         self.goal_handle_.abort()
        #     self.goal_active_ = True
        # #----------------------------------------------------------
        self.get_logger().info("accepting the goal!!")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle : ServerGoalHandle):
        self.get_logger().info("RECeieved a cancel request")
        return CancelResponse.ACCEPT  #or REJECT
    
    #queue goal handle
    # this function and execute callback function runs in series
    def handle_accepted_callback(self, goal_handle : ServerGoalHandle):
        #------------------------------------------------------------------------------------
        # POLICY : TO QUEUE GOALS
        #------------------------------------------------------------------------------------
        with self.goal_lock:
            if self.goal_handle_ is not None: # alreday a goal is running heress
                self.goal_queue_.append(goal_handle) #append all the upcomming heress goalss
            else:
                goal_handle.execute()  # this calls the execute callback
        #-------------------------------------------------------------------------------------
        #policy : preempt(terminate) exixting goal when receiving new goal
        #---------------------------------------------------------
        # with self.goal_lock:
        #     # if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #     if self.goal_handle_ is not None and self.goal_active_:
        #         self.get_logger().info("abort current goal and ACCEPTING THR NEW GOAL!!") 
        #         self.goal_handle_.abort()
        
        #     self.goal_active_ = True
        #     goal_handle.execute()
        #----------------------------------------------------------

    
    def execute_callback(self, goal_handle: ServerGoalHandle):
        #variable seperation while threading
        with self.goal_lock:
            #cancel duplicate goals
            self.goal_handle_ = goal_handle
            # if goal_handle.is_active:
            #     goal


        #Get request from the is goal!!
        target_number = goal_handle.request.target_number      # <target> = goal_handle.request.<action_goal_(the one we wrote in action file CountUntil.actiom)>) 
        period = goal_handle.request.period


        #execute the ACTion

        self.get_logger().info("executing the goal!!!!!!!!")
        #establish feedback
        Feedback = CountUntil.Feedback() #this feedback is inside the countuntil action that we wrote
        result = CountUntil.Result()
        counter = 0
        for i in range(target_number):
            #check wheather goal_handle is active in each thread(since each goal is running in each thread)(for preempting(terminating) the goal)
            if not goal_handle.is_active:
                result.reached_number = counter
                # run the next goal in queue
                self.process_next_goal_in_queue()
                self.goal_active_ = False
                return result
            #check if the goal cancel request is raised or wot
            if goal_handle.is_cancel_requested:
                self.get_logger().info("Cancelling the GOAl")
                #set goal handle as cancelled so goal gets cancelled
                goal_handle.canceled()
                result.reached_number = counter
                # run the next goal in queue
                self.process_next_goal_in_queue()
                # make sure no goal gets acceptied while the result of the first goal gets returned
                self.goal_active_ = False
                return result

            counter +=1
            # if counter == 3:
            #     goal_handle.abort()
            self.get_logger().info(f"counting: {counter}")
            Feedback.current_number = counter #current_number is inside the feedback section of the countuntil action that we wrote
            goal_handle.publish_feedback(Feedback)   #publish the feedback
            time.sleep(period)                                # time delay from Import time 

            # if counter == 3:
            #     break

        #once done,! set goal final state
        if target_number == counter:
            goal_handle.succeed()
            self.get_logger().info("goal Succeeded!!!!!!")
                        #now imediately right send the result
            # result = CountUntil.Result()            #Result  from CountUntil.action file
            # with self.goal_lock:
            #     if not goal_handle.is_active:
            #         self.get_logger().info('Goal aborted')
            #         return result

            # goal_handle.succeed()

            result.reached_number = counter     # Result < Reached_number comes under in action file
            # run the next goal in queue
            self.process_next_goal_in_queue()
            # make sure no goal gets acceptied while the result of the first goal gets returned
            self.goal_active_ = False
            return result                        #return the result is a mandatory otherwise it may throw errors at!

        else: # if goal couldnt be reached
            goal_handle.abort() # we can abort 
            self.get_logger().info("goal failed!!!!!!")

            # to cancel
            result.reached_number = counter
            self.process_next_goal_in_queue()
            # make sure no goal gets acceptied while the result of the first goal gets returned
            self.goal_active_ = False
            return result











    #process next goal in queue
    def process_next_goal_in_queue(self):
        with self.goal_lock:
            if len(self.goal_queue_) > 0:
                self.goal_queue_.pop(0).execute() # since it is an object of goalhandle: servergoalhandle
            else:
                self.goal_handle_ = None



def main(args = None):
    rclpy.init(args= args)
    node = CountUntilServer_Node()         #Modify  node_class_name heRE
    rclpy.spin(node, MultiThreadedExecutor()) # with this we can run multiple goals in parallel
    rclpy.shutdown()


if __name__ == "__main__":
    main()


### test in cli
#ros2 action send_goal /count_until my_robot_interfaces/action/CountUntil "{"target_number": 8, "period": 1.2}" --feedback



