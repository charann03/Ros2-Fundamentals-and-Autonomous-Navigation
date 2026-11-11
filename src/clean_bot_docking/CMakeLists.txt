cmake_minimum_required(VERSION 3.8)
project(clean_bot_docking)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(rclcpp REQUIRED)
find_package(apriltag_ros REQUIRED)
find_package(apriltag_msgs REQUIRED)
find_package(image_proc REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(tf2_ros REQUIRED)
# find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)
# Copy necessary files to designated locations in the project
install (
  DIRECTORY models worlds launch config scripts maps
  DESTINATION share/${PROJECT_NAME}
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
# Install Python executables
install(PROGRAMS
  scripts/test_detected_dock_pose_pub.py
  scripts/undock_custom.py
  scripts/test.py
  DESTINATION lib/${PROJECT_NAME}
)
# Install cpp executables

add_executable(detected_dock_pose_publisher scripts/detected_dock_pose_publisher.cpp) #executablename executable_file_path
ament_target_dependencies(detected_dock_pose_publisher
  rclcpp
  geometry_msgs
  tf2_ros
)
install(TARGETS
  detected_dock_pose_publisher
  DESTINATION lib/${PROJECT_NAME}
)


ament_package()
