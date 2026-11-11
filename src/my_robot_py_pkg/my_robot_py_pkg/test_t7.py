#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
# from threading import Event
# import keyboard as k
import time as t
from nav2_msgs.action import NavigateToPose
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor
from geometry_msgs.msg import PointStamped
from geometry_msgs.msg import PoseWithCovarianceStamped as pcs
from nav_msgs.msg import Odometry
from tf_transformations import euler_from_quaternion
# from std_msgs.msg import String
from pynput import keyboard

# import sys, select, termios, tty

# waypoints = [(2.0,1.5,1.0),(5.0,-1.12,1.0),(1.65,-3.58,1.0),(4.89,-1.09,1.0),(-4.65,3.69,1.0),(2.0,6.2,1.0)]
waypoints = []
# waypoints = [(2.0,1.5,1.0),(0.0,0.0,1.0),(2.0,1.5,1.0),(0.0,0.0,1.0),(2.0,1.5,1.0),(0.0,0.0,1.0)]
wait_time = [1 , 2 , 3, 4 , 5]
# press_key = "f"



# class Nav2ActionClient(Node):
#     def __init__(self):
#         super().__init__('nav2_action_client')
#         self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')
        
#     def send_goal(self , pos_points : tuple):
#         goal_msg = NavigateToPose.Goal()
#         goal_msg.pose.header.frame_id = 'map'
#         goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
#         goal_msg.pose.pose.position.x = pos_points[0]
#         goal_msg.pose.pose.position.y = pos_points[1]
#         goal_msg.pose.pose.orientation.w = pos_points[2]
        
#         self.action_client.wait_for_server()
#         self.future = self.action_client.send_goal_async(
#             goal_msg, 
#             # feedback_callback=self.feedback_callback
#             ).add_done_callback()
#         rclpy.spin_until_future_complete(self, self.future)
#         return self.future.result().status
#     def goal_response_callback()
        
#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')

#     def follow_waypoints(self, waypoints : list):
#         # for index in range(len(waypoints)-1):
#         #     if index == 0:
#         #         self.send_goal(waypoints[index])
#         #     if self.future.result().status == GoalStatus.STATUS_SUCCEEDED:
#         #         self.send_goal(waypoints[index])
#         #         self.get_logger().info("")            
#         #         self.get_logger().info(f"moving to waypoint{index +1, waypoints[index]}")
#         pass

    


# def main(args = None):
#     rclpy.init(args= args)
#     node = Nav2ActionClient()         #Modify  node_class_name heRE
#     node.follow_waypoints(waypoints)
#     rclpy.spin(node)

#     # executor = MultiThreadedExecutor()
#     rclpy.shutdown()


# if __name__ == "__main__":
#     main()

# class Nav2ActionClient(Node):
#     def __init__(self):
#         super().__init__('nav2_action_client')
#         # self.goal_handle_ : ClientGoalHandle = None
#         self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose',callback_group= ReentrantCallbackGroup())
#         # self.action_done_event = Event()
#         # self.goal_lock  = threading.Lock()

#     def send_goal(self , pos_points : tuple):
#         goal_msg = NavigateToPose.Goal()
#         goal_msg.pose.header.frame_id = 'map'
#         goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
#         goal_msg.pose.pose.position.x = pos_points[0]
#         goal_msg.pose.pose.position.y = pos_points[1]
#         goal_msg.pose.pose.orientation.w = pos_points[2]
        
#         while not self.action_client.wait_for_server(1.0):    #timeout 1 sec
#             self.get_logger().warn("waiting for navigatetoposes UntIL server......")      #warning message server
#         # SEND!! the GOal
#         self.get_logger().info("sending goal!!")
#         # self.action_done_event.clear()        
#         self.action_client.send_goal_async(
#             goal_msg, 
#             # feedback_callback=self.feedback_callback
#             ).add_done_callback(self.goal_response_callback)
#         # Wait for action to be done

#     def goal_response_callback(self, future):
#         self.goal_handle: ClientGoalHandle = future.result()
#         if self.goal_handle.accepted:
#             self.get_logger().info("GoAL got ACCepted")
#             self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
#         else:
#             self.get_logger().warn("GOAl got ReJeCtEd")
#         self.get_logger().info("wating for actioncompletion!!!!!!")



        


#     def goal_result_callback(self, future):
#         result = future.result().result      # THIS!! future.result().result --> this .result refers to the action result that we denoted in our action file!!
#         status = future.result().status
#         #check if the goal is SuCCEEDED
#         if status == GoalStatus.STATUS_SUCCEEDED:
#             self.get_logger().info("SuCCESS")
#             self.get_logger().info("action performed successfully")  
#             waypoints.pop(0)
#             if len(waypoints) >0:
#                 self.get_logger().info(f"{len(waypoints)}")
#                 self.send_goal(waypoints[0])          
#         #check if the goal is ABORted
#         elif status == GoalStatus.STATUS_ABORTED:
#             self.get_logger().fatal("ABORTED")
#         elif status == GoalStatus.STATUS_CANCELED:
#             self.get_logger().error("CANcelLED")
#         # self.get_logger().info(f"Result: {result.reached_number}")      # reached_number is under Result in action_file(CountUntil.action)!!!!!!
#         # self.action_done_event.set()

        
#     def feedback_callback(self, feedback_msg):
#         self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')

#     # def follow_waypoints(self, waypoints : list):
#     #     # for index in range(len(waypoints)-1):
#     #     #     if index == 0:
#     #     #         self.send_goal(waypoints[index])
#     #     #     if self.future.result().status == GoalStatus.STATUS_SUCCEEDED:
#     #     #         self.send_goal(waypoints[index])
#     #     #         self.get_logger().info("")            
#     #     #         self.get_logger().info(f"moving to waypoint{index +1, waypoints[index]}")
#     #     i = 0
#     #     for index in waypoints:
#     #         i+=1
#     #         self.send_goal(index)
#     #         # self.action_done_event.wait()
#     #         self.get_logger().info("wait is over")
#     #         self.get_logger().info(f"moving to {i} point")

    


# def main(args = None):
#     rclpy.init(args= args)
#     node = Nav2ActionClient()         #Modify  node_class_name heRE
#     node.send_goal(waypoints[0])
#     # node.follow_waypoints(waypoints)
#     rclpy.spin(node, MultiThreadedExecutor())

#     # executor = MultiThreadedExecutor()
#     rclpy.shutdown()


class Nav2ActionClient(Node):
    def __init__(self):
        super().__init__('nav2_action_client')
        # self.goal_handle_ : ClientGoalHandle = None
        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose',callback_group= ReentrantCallbackGroup())
        self.pub_pts = self.create_subscription(PointStamped , "/clicked_point",self.append_pts, 10)
        # self.get_logger().info("set home posn!!!!!")
        self.home_pos_rec = self.create_subscription(Odometry, "/odom",self.rec_home_pos,10 )
        self.amcl_received = False
        self.initial_pose_sent = False
        self.amcl_pose_sub = self.create_subscription(pcs, "/amcl_pose" ,self.amcl_callback, 10)
        self.initial_pose_pub = self.create_publisher(pcs, "/initialpose", 10)
        self.timer = self.create_timer(1.0, self.check_amcl)
        # self.action_done_event = Event()
        # self.goal_lock  = threading.Lock()
        # if len(waypoints) > 0:
        # self.press_key = self.create_subscription(String, "/teleopkeys" ,self.key_pressed,10 )
        self.fnc_iter = 1
        # self.key_interrupt()
        self.inc = 0
        self.home_inc = 1

    def amcl_callback(self, msg : pcs):
        self.amcl_received = True

    # def pub_intial_pose(self , msg: pcs):
    #     if msg.pose.pose is None:
    #         msg_ = pcs()
    #         msg_.header.stamp = self.get_clock().now().to_msg()
    #         msg_.header.frame_id = "map"
    #         msg_.pose.pose.position.x = 0.0
    #         msg_.pose.pose.position.y = 0.0
    #         msg_.pose.pose.orientation.w = 1.0
    #         msg_.pose.pose.orientation.z = 0.0
    #         self.get_logger().info("publishing initial pose!!")
    #         self.initial_pose_pub.publish(msg_)

    def check_amcl(self):
        if not self.amcl_received and not self.initial_pose_sent:
            self.get_logger().warn("AMCL pose not received → publishing initial pose")

            msg_ = pcs()
            msg_.header.stamp = self.get_clock().now().to_msg()
            msg_.header.frame_id = "map"

            msg_.pose.pose.position.x = 0.0
            msg_.pose.pose.position.y = 0.0

            msg_.pose.pose.orientation.z = 0.0
            msg_.pose.pose.orientation.w = 1.0

            self.initial_pose_pub.publish(msg_)
            self.initial_pose_sent = True


    def append_pts(self, msg : PointStamped):
        self.x  = msg.point.x
        self.y = msg.point.y
        self.yaw = 1.0 
        waypoints.append((self.x , self.y , self.yaw))
        self.inc +=1
        self.get_logger().info(f"appending waypoint {self.inc} is {waypoints[self.inc -1] }")
        # if len(waypoints) == 1:
        #     self.get_logger().info("home posnss have been set!!!")
        # self.key_interrupt()
        # global key
        # key = str(input())
    # def key_pressed(self, msg_: String):
    #     # global key
    #     self.key = msg_.data
    #     # self.key_interrupt()
    #     self.get_logger().info(f"pressed {self.key}")
    #     if self.key == "p_space" and self.fnc_iter == 1:
    #         self.get_logger().info("waypoint follower started")
    #         self.follow_waypoints(waypoints)
    #     else:
    #         pass

    # def key_pressed_test(self):
    #     self.key_prs = self.key_interrupt()
    #     # self.get_logger().info(f"pressed: {self.key_prs}")
    #     self.get_logger().info(f"pressed {self.key_prs}")
    #     if str(self.key_prs) == "Key.space" and self.fnc_iter == 1:
    #         self.get_logger().info("waypoint follower started")
    #         self.follow_waypoints(waypoints)
    #     else:
    #         pass


    def rec_home_pos(self, msg__: Odometry):
        if len(waypoints) == 0 and self.fnc_iter == 1:
            self.x_ = msg__.pose.pose.position.x
            self.y_ = msg__.pose.pose.position.y
            self.qz_ = msg__.pose.pose.orientation.z
            self.qw_ = msg__.pose.pose.orientation.w
            self.yaw_ = euler_from_quaternion([0.0 , 0.0 , self.qz_ , self.qw_])
            self.home_pos_odom = (self.x_ , self.y_ , self.yaw_[2])
        if self.fnc_iter > 1 and len(waypoints) == 0 and self.home_inc == 1:
            self.get_logger().info(f"home posn is : {self.home_pos_odom}")
            self.get_logger().info("going to home posn")
            self.send_goal(self.home_pos_odom)
            self.home_inc +=1
        else:
            pass
            
            

        

    def send_goal(self , pos_points : tuple):
        # self.first_pnt = waypoints[0]
        goal_msg = NavigateToPose.Goal()
        goal_msg.pose.header.frame_id = 'map'
        goal_msg.pose.header.stamp = self.get_clock().now().to_msg()
        goal_msg.pose.pose.position.x = pos_points[0]
        goal_msg.pose.pose.position.y = pos_points[1]
        goal_msg.pose.pose.orientation.w = pos_points[2]
        
        while not self.action_client.wait_for_server(1.0):    #timeout 1 sec
            self.get_logger().warn("waiting for navigatetoposes UntIL server......")      #warning message server
        # SEND!! the GOal
        self.get_logger().info("sending goal!!")
        # self.action_done_event.clear()        
        self.action_client.send_goal_async(
            goal_msg, 
            # feedback_callback=self.feedback_callback
            ).add_done_callback(self.goal_response_callback)
        # Wait for action to be done

    def goal_response_callback(self, future):
        self.goal_handle: ClientGoalHandle = future.result()
        if self.goal_handle.accepted:
            self.get_logger().info("GoAL got ACCepted")
            self.goal_handle.get_result_async().add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn("GOAl got ReJeCtEd")
        self.get_logger().info("wating for actioncompletion!!!!!!")



        


    def goal_result_callback(self, future ):
        result = future.result().result      # THIS!! future.result().result --> this .result refers to the action result that we denoted in our action file!!
        status = future.result().status
        #check if the goal is SuCCEEDED
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("SuCCESS")
            self.get_logger().info("action performed successfully")
            self.get_logger().info(f"waiting for {wait_time[0]}seconds")
            t.sleep(wait_time[0])



            # if len(waypoints) == 1:
            #     self.get_logger().info("going to home posnss!!!!!!")
            if len(waypoints) >0:
                self.get_logger().info(f"{len(waypoints) , waypoints[0]}")                
                waypoints.pop(0)
                wait_time.pop(0)

                try:
                    self.send_goal(waypoints[0])
                except IndexError:
                    pass
            
          
        #check if the goal is ABORted
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().fatal("ABORTED")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().error("CANcelLED")
        # self.get_logger().info(f"Result: {result.reached_number}")      # reached_number is under Result in action_file(CountUntil.action)!!!!!!
        # self.action_done_event.set()
        # self.get_logger().info(f"waiting for {wait_time[0]}seconds")
        # t.sleep(wait_time[0])

        
    def feedback_callback(self, feedback_msg):
        self.get_logger().info(f'Received feedback: {feedback_msg.feedback}')

    def follow_waypoints(self, waypoints : list):
        # for index in range(len(waypoints)-1):
        #     if index == 0:
        #         self.send_goal(waypoints[index])
        #     if self.future.result().status == GoalStatus.STATUS_SUCCEEDED:
        #         self.send_goal(waypoints[index])
        #         self.get_logger().info("")            
        #         self.get_logger().info(f"moving to waypoint{index +1, waypoints[index]}")
        # i = 0
        # for index in waypoints:
        #     i+=1
        #     self.send_goal(index)
        #     # self.action_done_event.wait()
        #     self.get_logger().info("wait is over")
        #     self.get_logger().info(f"moving to {i} point")
        if self.fnc_iter == 1:
            # self.home_pos = waypoints[0]
            # waypoints.pop(0)
            # waypoints.append(self.home_pos)
            self.get_logger().info("{ , waypoints[0]}")
            self.send_goal(waypoints[0])
            self.fnc_iter +=1

    def key_interrupt(self):
        # if key == "p_space" and self.fnc_iter == 1:
        #     self.get_logger().info("waypoint follower started")
        #     self.follow_waypoints(waypoints)
        # else:
        # pass
        def on_press(key, injected):

            # self.get_logger().info(f"pressed {key}")
            if str(key) == "Key.space" and self.fnc_iter == 1:
                self.get_logger().info("waypoint follower started")
                self.follow_waypoints(waypoints)
            else:
                pass


        def on_release(key, injected):
            # print('{} released; it was {}'.format(
            #     key, 'faked' if injected else 'not faked'))
            if key == keyboard.Key.esc:
                # Stop listener
                return False

        # # Collect events until released
        # with keyboard.Listener(
        #         on_press=on_press,
        #         on_release=on_release) as listener:
        #     listener.join()

        # ...or, in a non-blocking fashion:
        listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release)
        listener.start()






    


def main(args = None):
    # def getKey():
    #     # settings = termios.tcgetattr(sys.stdin)
    #     tty.setraw(sys.stdin.fileno())
    #     rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    #     if rlist:
    #         key = sys.stdin.read(1)
    #     else:
    #         key = ''

    #     termios.tcsetattr(sys.stdin, termios.TCSADRAIN,settings)
    #     return key
    # settings = termios.tcgetattr(sys.stdin)
    rclpy.init(args= args)
    node = Nav2ActionClient()         #Modify  node_class_name heRE
    # node.send_goal(waypoints)
    # settings = termios.tcgetattr(sys.stdin)
    # node.append_pts()
    # key = getKey()
    # while key == press_key:
    # while True:
    #     try:
    #         print("press f key to quit waypoint")
    #         t.sleep(0.5)
    #     except key == press_key:
    #         break


    # print(f"length of listss: {len(waypoints)}")
    # if len(waypoints) == 6:
    #     node.follow_waypoints(waypoints)
    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)

    node.key_interrupt()

    rclpy.spin(node, MultiThreadedExecutor())

    # executor = MultiThreadedExecutor()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

