cmake_minimum_required(VERSION 3.8)
project(my_robot_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()



# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(my_robot_interfaces REQUIRED)


#adding executables
add_executable(cpp_node src/my_first_node.cpp) #node name followed by absolute path locations
ament_target_dependencies(cpp_node rclcpp) #node name followed by dependencies

add_executable(robot_publisher src/robot_news_publisher.cpp)
ament_target_dependencies(robot_publisher
                          rclcpp
                          example_interfaces)

add_executable(robot_subscriber src/robot_news_subscriber.cpp)
ament_target_dependencies(robot_subscriber
                          rclcpp
                          example_interfaces)

add_executable(add_two_ints_server src/add_two_ints_server.cpp)
ament_target_dependencies(add_two_ints_server
                          rclcpp
                          example_interfaces)

add_executable(add_two_ints_client_no_oops src/add_two_ints_client_no_oop.cpp)
ament_target_dependencies(add_two_ints_client_no_oops
                          rclcpp
                          example_interfaces)

add_executable(add_two_ints_client src/add_two_ints_client.cpp)
ament_target_dependencies(add_two_ints_client
                          rclcpp
                          example_interfaces)

add_executable(hw_status_publisher src/hardware_status_publisher.cpp)
ament_target_dependencies(hw_status_publisher
                          rclcpp
                          example_interfaces
                          my_robot_interfaces)
                      
add_executable(led_panel_node src/led_panel_node.cpp)
ament_target_dependencies(led_panel_node
                          rclcpp
                          example_interfaces
                          my_robot_interfaces)

add_executable(battery_node src/battery_node.cpp)
ament_target_dependencies(battery_node
                          rclcpp
                          example_interfaces
                          my_robot_interfaces)

add_executable(number_publisher src/number_publisher.cpp)
ament_target_dependencies(number_publisher
                          rclcpp
                          example_interfaces)

add_executable(subscribe src/subscribe.cpp)
ament_target_dependencies(subscribe
                          rclcpp
                          example_interfaces)

add_executable(testcpp src/test.cpp)
ament_target_dependencies(testcpp
                          rclcpp
                          example_interfaces)


add_executable(service_test src/service_test.cpp)
ament_target_dependencies(service_test
                          rclcpp
                          example_interfaces)

add_executable(count_until_server_cpp src/count_until_server.cpp )
ament_target_dependencies(count_until_server_cpp
                          rclcpp
                          rclcpp_action
                          my_robot_interfaces)

add_executable(count_until_client_cpp src/count_until_client.cpp )
ament_target_dependencies(count_until_client_cpp
                          rclcpp
                          rclcpp_action
                          my_robot_interfaces)


add_executable(count_until_server_queue_goals src/count_until_server_queue_goals.cpp )
ament_target_dependencies(count_until_server_queue_goals
                          rclcpp
                          rclcpp_action
                          my_robot_interfaces)


add_executable(control_robot_server src/control_robot_server.cpp )
ament_target_dependencies(control_robot_server
                          rclcpp
                          rclcpp_action
                          my_robot_interfaces)


add_executable(control_robot_client src/control_robot_client.cpp )
ament_target_dependencies(control_robot_client
                          rclcpp
                          rclcpp_action
                          my_robot_interfaces
                          example_interfaces
                          )



install(TARGETS
  cpp_node  # node name
  robot_publisher          # we can add any upcomming executables
  robot_subscriber
  add_two_ints_server
  add_two_ints_client_no_oops
  add_two_ints_client
  hw_status_publisher
  led_panel_node
  battery_node
  number_publisher
  testcpp
  subscribe
  service_test
  count_until_server_cpp
  count_until_client_cpp
  count_until_server_queue_goals
  control_robot_server
  control_robot_client

  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
