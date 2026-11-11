from launch import LaunchDescription
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode

def generate_launch_description():
    ld = LaunchDescription()
    container = ComposableNodeContainer(
        name="components_cpp_container",
        namespace="",
        package= "rclcpp_components",
        executable= "component_container", # single threaded executor
        composable_node_descriptions= [
            ComposableNode(
                package= "components_cpp",
                plugin= "components_cpp::NumberPublisher",
                name= "Number_PUblisher_1"
            ),
            ComposableNode(
                package= "components_cpp",
                plugin= "components_cpp::NumberPublisher",
                name= "number_pubisher_2"
            ),
            ComposableNode(
                package= "components_cpp",
                plugin= "components_cpp::NumberPublisher",
                name= "number_pubisher_3"
            )
        ]
    )
    ld.add_action(container)


    return ld