#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle
from nav2_msgs.action import NavigateToPose
import time as t
import threading

waypoints = [(2.0,1.5,1.0),(4.5,-2.57,1.0),(-4.5,2.14,1.0),(0.0,1.5,1.0),(4.95,5.04,1.0),(2.0,6.2,1.0)]
home_pose = (0.0,0.0,1.0)
wait_time = [1.0 , 2.0 , 3.0 , 4.0 , 5.0 ]
waypoints_flag = False
goal_pass_flag = False

class Nav2ActionClient(Node):
    def __init__(self):
        super().__init__('nav2_action_client')
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        # self.goal_done_event = threading.Event()
        # self.action_done_event = Event()
    def send_goal(self,pos_points: tuple):
        # self.action_done_event.clear()
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = pos_points[0]
        goal_msg.pose.pose.position.y = pos_points[1]
        goal_msg.pose.pose.orientation.w = pos_points[2]
        # goal_msg.pose.pose.orientation.z = 0.0
        
        self.action_client.wait_for_server()
        # future = self.action_client.send_goal_async(
        #     goal_msg, feedback_callback=self.goal_response_callback)
        # return future
        self._send_goal_future = self.action_client.send_goal_async(
    goal_msg,
    #feedback_callback=self.feedback_callback
    )

        self._send_goal_future.add_done_callback(self.goal_response_callback)
    
        # # Wait for action to be done
        # self.action_done_event.wait()
        # return goal_pass_flag == True
    
    def goal_response_callback(self, future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info("GoAL got ACCepted")

            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn("GOAl got ReJeCtEd")
        # self.get_logger().info(f"{self.goal_handle._goal_response}")
        # self.get_logger().info(f"{self.goal_handle._status}")

    def goal_result_callback(self, future):
        # # Signal that action is done
        # self.action_done_event.set()

        result = future.result().result   # THIS!! future.result().result --> this .result refers to the action result that we denoted in our action file!!  
        status = future.result().status
        if status == 4:

            goal_pass_flag = True
            self.get_logger().info(f"Result: GOAl succeeded {result.result} ")      # reached_number is under Result in action_file(CountUntil.action)!!!!!!
            self.get_logger().info(f"Result: GOAl outoput {goal_pass_flag} ")      # reached_number is under Result in action_file(CountUntil.action)!!!!!!
            self.get_logger().info(f"Status: {status}")
            self.goal_done_event.set()
            return goal_pass_flag
        else:
            self.get_logger().info(f"Result: GOAl failed {result.result} ")      # reached_number is under Result in action_file(CountUntil.action)!!!!!!
            goal_pass_flag == False
            return goal_pass_flag


        

        
    # def feedback_callback(self, feedback_msg):
    #     self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')
    #     # pass
    # def followwaypoint(self, waypoints: list, time_interval: list):
    #     while self.action_client.wait_for_server():
    #         self.send_goal(waypoints[0])
    #         t.sleep(time_interval[0])
    #         self.get_logger().info(f"goal_flag: {goal_pass_flag}")
    #         for index in range(len(waypoints)-1):
    #             # if points == waypoints[0]:
    #             #     continue
    #             # if goal_pass_flag == True:
    #             #     self.send_goal(points)
    #             # else:
    #             #     self.get_logger().info(f"goal failed at ")
    #             if goal_pass_flag == True:
    #                 self.send_goal(waypoints[index+1])
    #                 t.sleep(time_interval[index+1])
    #                 if index +1 == len(waypoints)-1:
    #                     waypoints_flag == True
    #                     self.go_to_home()
    #             else:
    #                 self.get_logger().info(f"goal failed at {index +2} waypoint {waypoints[index+1]}")
    #                 break
    #         break
    def followwaypoint(self, waypoints: list, time_interval: list):
        self.send_goal(waypoints[0])
        t.sleep(time_interval[0])
        

        for index in range(len(waypoints)-1):
            # self.goal_done_event.wait()
            self.get_logger().info(f"goal_flag: {goal_pass_flag}")
            # if points == waypoints[0]:
            #     continue
            # if goal_pass_flag == True:
            #     self.send_goal(points)
            # else:
            #     self.get_logger().info(f"goal failed at ")
            if goal_pass_flag == True:
                self.send_goal(waypoints[index+1])
                t.sleep(time_interval[index+1])
                goal_pass_flag = False
                if index +1 == len(waypoints)-1:
                    waypoints_flag = True
                    return waypoints_flag
            else:
                self.get_logger().info(f"goal failed at {index +2} waypoint {waypoints[index+1]}")
                break








    def go_to_home(self):
        if waypoints_flag == True:
            self.send_goal(home_pose)



def main(args = None):
    rclpy.init(args= args)
    node = Nav2ActionClient()         #Modify  node_class_name heRE
    node.followwaypoint(waypoints,wait_time)
    node.go_to_home()

    # executor = MultiThreadedExecutor()
    rclpy.spin(node
    # ,executor
    )
    rclpy.shutdown()


if __name__ == "__main__":
    main()




