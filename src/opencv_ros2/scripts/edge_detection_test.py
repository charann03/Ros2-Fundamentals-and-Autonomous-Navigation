# #!/usr/bin/env python3

# import rclpy
# from rclpy.node import Node
# import cv2
# from cv_bridge import CvBridge , CvBridgeError
# from sensor_msgs.msg import Image

# class LoadImage(Node):  #Modify node_class_name heRe

#     def __init__(self):
#         super().__init__("Edge_Detection_Node")   #Modify node_mame heRe
#         # self.picture = picture
#         self.image_sub = self.create_subscription(Image, "/camera/image_raw", self.camera_callback, 10)
#         self.bridge_object = CvBridge()


#     def camera_callback(self ,data: Image):
#         try:

#             cv_image = self.bridge_object.imgmsg_to_cv2(img_msg= data, desired_encoding="bgr8")  
#         except CvBridgeError as e:
#             print(e)

#         cv2.imshow('image_output', cv_image)
#         # cv2.waitKey(0) #waits forever and gets terminated only if 0 is pressesd on the image window
#         cv2.waitKey(1) #waits 1 millisecond and moves to the next line of code ,so nade can be terminated by ctrl+c in terminal
# #for proper shutdown node
# def main(args=None):
#     rclpy.init(args=args)

#     node = LoadImage()

#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         node.get_logger().info("Shutting down...")
#     finally:
#         node.destroy_node()
#         cv2.destroyAllWindows()

#         if rclpy.ok():
#             rclpy.shutdown()


# if __name__ == "__main__":
#     main()


import cv2
import numpy as np

img = cv2.imread("/home/charann-inc5751/ros2_ws/src/opencv_ros2/images/input/cobot.png")
#size of image
rows, cols, _ = img.shape
print("rows", rows) # rows up to down 
print("colsss", cols) #columns left to right
print("channel", _)

#crop image
# crop_image = img[174:280, 0:348] #[rows start index: rows_stop_index, column_start_index: column_stop_index]

#ROI (region of intrest)
cv2.rectangle(img,(100, 10), (248, 338), (0, 255, 0), 6 ) #(x1,y1),(x2,y2)-> opposite vertices , (r, g, b/255), line_width in pixels= 6
roi = img[10: 338, 100:248 ] #(x1:x2, y1:y2)
cv2.imshow("cropped_image_IS", roi)
cv2.imshow("image", img)
cv2.waitKey(0)
