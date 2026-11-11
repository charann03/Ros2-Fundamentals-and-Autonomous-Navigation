#!/bin/bash

source ~/anaconda3/etc/profile.d/conda.sh
conda activate yolo-ros

source /opt/ros/humble/setup.bash
source ~/ros2_ws/install/setup.bash

exec ros2 run opencv_ros2 object_detection