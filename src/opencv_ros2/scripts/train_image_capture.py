#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import cv2
from cv_bridge import CvBridge , CvBridgeError
from sensor_msgs.msg import Image

class train_image_capture(Node):  #Modify node_class_name heRe

    def __init__(self):
        super().__init__("train_image_capture_node")   #Modify node_mame heRe
        self.image_sub = self.create_subscription(Image, "/camera/image_raw", self.camera_callback, 10)
        self.bridge_object = CvBridge()
        self.image_cnt = 0 
        self.last_save_time = self.get_clock().now().nanoseconds / 1e9

    def camera_callback(self, data:Image):
        
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

        cv2.imshow("Camera", cv_image)
        cv2.waitKey(1)
        img_path = "/home/charann-inc5751/ros2_ws/src/opencv_ros2/train_master"
        current_time = self.get_clock().now().nanoseconds / 1e9

        if current_time - self.last_save_time >= 1.0:

            cv2.imwrite(
                img_path + f"/master{self.image_cnt}.png",
                cv_image
            )

            self.get_logger().info(f"Saved master{self.image_cnt}.png")

            self.image_cnt += 1
            self.last_save_time = current_time


#for proper shutdown node
def main(args=None):
    rclpy.init(args=args)

    node = train_image_capture()

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




