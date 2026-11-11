cmake_minimum_required(VERSION 3.8)
project(sub_pub)

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(cpp_node
    cpp/talker.cpp
)

ament_target_dependencies(cpp_node
    rclcpp
    std_msgs
)

install(TARGETS
    cpp_node
    DESTINATION lib/${PROJECT_NAME}
)

ament_package()