#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
# when using multithrededexecutors mustusea callback group
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
import time



class Node1(Node):
    def __init__(self):
        super().__init__("node1")
        #create a callback group object heress
        self.cb_group_ = ReentrantCallbackGroup() # enables the timers to run in parallel
        #must add the callback group object
        # to run callback in one thread and callback 2 and callback 3 together in another thread
        self.cb_group_1 = MutuallyExclusiveCallbackGroup()
        self.cb_group_2 = MutuallyExclusiveCallbackGroup()
        # self.cb_group_3 = MutuallyExclusiveCallbackGroup()


        self.timer1_ = self.create_timer(1.0, self.callback_timer1, callback_group=self.cb_group_1) # its like a single threaded executor inside a multi threaded executor
        self.timer2_ = self.create_timer(1.0, self.callback_timer2,callback_group=self.cb_group_2)
        self.timer3_ = self.create_timer(10.0, self.callback_timer3,callback_group=self.cb_group_2)

    def callback_timer1(self):
        time.sleep(2.0)
        self.get_logger().info("cb 1")

    def callback_timer2(self):
        time.sleep(2.0)
        self.get_logger().info("cb 2")

    def callback_timer3(self):
        time.sleep(2.0)
        self.get_logger().info("cb 3")

class Node2(Node):
    def __init__(self):
        super().__init__("node2")
        self.cb_group_ = ReentrantCallbackGroup()
        self.timer4_ = self.create_timer(1.0, self.callback_timer4, callback_group=self.cb_group_)
        self.timer5_ = self.create_timer(1.0, self.callback_timer5, callback_group=self.cb_group_)
        self.timer6_ = self.create_timer(1.0, self.callback_timer6,callback_group=self.cb_group_)

    def callback_timer4(self):
        time.sleep(2.0)
        self.get_logger().info("cb 4")

    def callback_timer5(self):
        time.sleep(2.0)
        self.get_logger().info("cb 5")

    def callback_timer6(self):
        time.sleep(2.0)
        self.get_logger().info("cb 6")


def main(args=None):
    rclpy.init(args=args)
    node1 = Node1()
    node2 = Node2()
    executor = MultiThreadedExecutor() # default mutuallyexclusivecallbackgroup
    executor.add_node(node1)
    executor.add_node(node2)
    executor.spin()
    # rclpy.spin(node1, executor= MultiThreadedExecutor())
    rclpy.shutdown()


if __name__ == "__main__":
    main()
