import cv2 
import numpy as np
import matplotlib.pyplot as plt
import os


# def contours():
#     # root = os.getcwd()
#     # img_path = os.path.join(root,)
#     img_path = "/home/charann-inc5751/ros2_ws/src/opencv_ros2/images/input/cobot.png"
#     img = cv.imread(img_path, cv.IMREAD_GRAYSCALE)
#     #crop the image if needed
#     # roi = img[10: 338, 100:248 ] #(x1:x2, y1:y2)
#     plt.figure()
#     plt.subplot(231)
#     plt.imshow(img, cmap="gray")
#     plt.show()

#     #scale the image
#     height, width = img.shape
#     scale = 4
#     height_scale = int(scale*height)
#     widthscale = int(scale*width)
#     img = cv.resize(img, (widthscale, height_scale))
#     _,thresh = cv.threshold(img,)
#     plt.show


# if __name__ == "__main__":
#     contours()

# image = cv2.imread('/home/charann-inc5751/ros2_ws/src/opencv_ros2/images/input/cobot.png')
# # cv2.waitKey(0)
# #convert img to grayscale
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# # cv2.imshow("gray", gray)
# # cv2.waitKey(0)
# edged = cv2.Canny(gray, 30, 200)
# # cv2.waitKey(0)
# contours, hierarchy = cv2.findContours(edged,
#                       cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# cv2.imshow('Canny Edges After Contouring', edged)
# cv2.waitKey(0)



image = cv2.imread('/home/charann-inc5751/ros2_ws/src/opencv_ros2/images/input/cobot.png')
# cv2.waitKey(0)
#convert img to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# apply binary thresholding
#  Binary Threshold (cv2.THRESH_BINARY)

#     If a pixel’s intensity is above the threshold, it is assigned the maximum value (usually 255; white)—otherwise, it becomes 0 (black).
#     Useful for separating bright objects from a dark background.

#  Binary Threshold Inverted (cv2.THRESH_BINARY_INV))

#     This works opposite to the binary threshold. Pixels above the threshold become 0 (black), and those below become the maximum value (255; white).
#     Highlights background over foreground.
ret, thresh = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY_INV) #(graycale_image, threshold_value, maximum_value, operation_type)
cv2.imshow("binary_image", thresh)
# cv2.waitKey(0)

# detect the contours on the binary image using cv2.CHAIN_APPROX_NONE
contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
print("contours"," : ", contours)     
print("hierarchy", " : ", hierarchy)
print(len(hierarchy[0]))                  
# draw contours on the original image
image_copy = image.copy()
# if hierarchy[0][0][3] == -1:
#     print("printing"," : ", hierarchy[0][0][3] )
#contours[0] just to print the outermost contour of the object
cv2.drawContours(image=image_copy, contours=contours[0], contourIdx=-1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)
                
# see the results
cv2.imshow('None approximation', image_copy)
cv2.waitKey(0)
#save the output image in it
# cv2.imwrite('contours_none_image1.jpg', image_copy)
cv2.destroyAllWindows()


