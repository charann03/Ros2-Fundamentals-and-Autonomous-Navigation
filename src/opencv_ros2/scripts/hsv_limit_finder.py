import cv2 as cv
import numpy as np

img = cv.imread("/home/charann-inc5751/ros2_ws/src/opencv_ros2/images/output/camera_output.png")
clone = img.copy()

drawing = False
ix, iy = -1, -1
roi_selected = False


def get_hsv_range(roi):
    hsv_roi = cv.cvtColor(roi, cv.COLOR_BGR2HSV)

    pixels = hsv_roi.reshape((-1, 3))

    # Most frequent HSV value
    unique, counts = np.unique(pixels, axis=0, return_counts=True)
    dominant_hsv = unique[np.argmax(counts)]

    h, s, v = dominant_hsv

    lower = [
        max(h - 10, 0),
        max(s - 40, 0),
        max(v - 40, 0)
    ]

    upper = [
        min(h + 10, 179),
        min(s + 40, 255),
        min(v + 40, 255)
    ]

    print("\nDominant HSV:", dominant_hsv)
    print("Lower HSV:", lower)
    print("Upper HSV:", upper)


def mouse_callback(event, x, y, flags, param):
    global ix, iy, drawing, img, clone

    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_LBUTTONUP:
        drawing = False

        cv.rectangle(img, (ix, iy), (x, y), (0, 255, 0), 2)

        x1 = min(ix, x)
        x2 = max(ix, x)
        y1 = min(iy, y)
        y2 = max(iy, y)

        roi = clone[y1:y2, x1:x2]

        if roi.size > 0:
            get_hsv_range(roi)


cv.namedWindow("Image")
cv.setMouseCallback("Image", mouse_callback)

while True:
    cv.imshow("Image", img)

    key = cv.waitKey(1) & 0xFF

    if key == 27:
        break

cv.destroyAllWindows()