#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge , CvBridgeError
from sensor_msgs.msg import Image
import numpy as np

class LoadImage(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("Load_Image_Node")   #Modify node_mame heRe
        # self.picture = picture
        self.image_sub = self.create_subscription(Image, "/camera/image_raw", self.camera_callback, 10)
        self.bridge_object = CvBridge()


    def camera_callback(self ,data: Image):
        try:
            """this function takes image data from ros
             and makes opencv compatible make
             sure the image encoding is
             same as the encoding that we give in the 
            camera plugin in urdf ie.. for depth camera
             we give B8G8R8 so her it becomes bgr8"""
            
            cv_image = self.bridge_object.imgmsg_to_cv2(img_msg= data, desired_encoding="bgr8")  
        except CvBridgeError as e:
            print(e)
        cv2.imshow("camera_no_filters", cv_image)
        #laplacian filter detection
        laplacian = cv2.Laplacian(cv_image, cv2.CV_64F) #64 bitfloat datatype bclack and white
        laplacian = np.uint8(laplacian) #convert from float to 8 bit integer
        cv2.imshow("laplacian", laplacian)

        #canny edge detection
        edges = cv2.Canny(cv_image, 150, 150 ) #100, 100 are thresholds more thresholds less details, less thresholds more details
        cv2.imshow("canny_edge", edges)

        
        # cv2.waitKey(0) #waits forever and gets terminated only if 0 is pressesd on the image window
        cv2.waitKey(1) #waits 1 millisecond and moves to the next line of code ,so nade can be terminated by ctrl+c in terminal
#for proper shutdown node
def main(args=None):
    rclpy.init(args=args)

    node = LoadImage()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("Shutting down...")
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()

