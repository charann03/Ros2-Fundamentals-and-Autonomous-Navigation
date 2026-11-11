cmake_minimum_required(VERSION 3.8)
project(opencv_ros2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
install (
  DIRECTORY scripts launch bash_scripts
  DESTINATION share/${PROJECT_NAME}
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
# Install Python executables
install(PROGRAMS
  scripts/load_image
  scripts/load_image_from_camera
  scripts/color_filtering
  scripts/edge_detection_test.py
  scripts/edge_detection
  scripts/object_detection
  scripts/custom_edge_detection
  scripts/train_image_capture.py
  scripts/camera_to_world
  scripts/canny_edge_detection.py
  scripts/object_pose_detection

  DESTINATION lib/${PROJECT_NAME}
)

# add_executable(load_img scripts/load_image.py) #executablename executable_file_path


ament_package()
