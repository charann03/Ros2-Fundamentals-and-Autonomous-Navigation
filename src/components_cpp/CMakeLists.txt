cmake_minimum_required(VERSION 3.8)
project(components_cpp)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
#for componenets
find_package(rclcpp_components REQUIRED)
find_package(example_interfaces REQUIRED)
#must add this line if new directory is been addeds
include_directories(include)

#for componenets
add_library(number_pub_component SHARED src/number_publisher.cpp)
ament_target_dependencies(number_pub_component rclcpp rclcpp_components example_interfaces)

#register the componenet
rclcpp_components_register_nodes(number_pub_component "components_cpp::NumberPublisher")

add_executable(manual_composition src/manual_composition.cpp)
ament_target_dependencies(manual_composition rclcpp)

#install components library
install(TARGETS
  number_pub_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
  )



install(TARGETS
  manual_composition
  DESTINATION lib/${PROJECT_NAME}/
)

# for launch files
install(DIRECTORY
  launch
  DESTINATION share/${PROJECT_NAME}/
)

ament_package()
