cmake_minimum_required(VERSION 3.8)
project(clean_bot)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

install(
  DIRECTORY launch urdf rviz params maps world models
  DESTINATION share/${PROJECT_NAME}/
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
# Install Python executables
install(PROGRAMS
  scripts/test_t8.py
  scripts/waypoint_t8.py
  scripts/f2c_ros_cb.py
  scripts/path_follower.py
  scripts/path_to_route.py
  scripts/route_follower.py
  scripts/follow_path.py
  scripts/foll_path_tes.py
  scripts/test_path_pub.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
