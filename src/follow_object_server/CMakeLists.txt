cmake_minimum_required(VERSION 3.8)
project(follow_object_server)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
# uncomment the following section in order to fill in
# further dependencies manually.
# find_package(<dependency> REQUIRED)

find_package(ament_cmake_python REQUIRED)
find_package(rclpy REQUIRED)

install(
  DIRECTORY launch params meshes scripts urdf models
  DESTINATION share/${PROJECT_NAME}/
)

# Install Python modules
ament_python_install_package(${PROJECT_NAME})
# Install Python executables
install(PROGRAMS
  scripts/follow_object_client.py
  scripts/artag_pose.py
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
