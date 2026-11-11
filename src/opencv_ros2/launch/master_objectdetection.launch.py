# NOTE: to run the yolo object_detection scripts create a bash script implementing the conda environment and add the objectdetection script file
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():

    return LaunchDescription([
        ExecuteProcess(
            # object_detection script file for master_robot
            cmd=["/home/charann-inc5751/ros2_ws/src/opencv_ros2/bash_scripts/master_object_detection.sh"],
            output="screen"
        )
    ])