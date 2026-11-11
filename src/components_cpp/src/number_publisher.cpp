#include "rclcpp/rclcpp.hpp"
// #include "example_interfaces/msg/int64.hpp"
#include "components_cpp/number_publisher.hpp"

using namespace std::chrono_literals;

namespace components_cpp{

    NumberPublisher::NumberPublisher(const rclcpp::NodeOptions &options) : Node("number_publisher", options)
    {
        number_ = 2;

        number_publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number", 10);
        number_timer_ = this->create_wall_timer(1000ms,
                                                std::bind(&NumberPublisher::publishNumber, this));
        RCLCPP_INFO(this->get_logger(), "Number publisher has been started.");
    }


    void NumberPublisher::publishNumber()
    {
        auto msg = example_interfaces::msg::Int64();
        msg.data = number_;
        number_publisher_->publish(msg);
    }

}


// int main(int argc, char **argv)
// {
//     rclcpp::init(argc, argv);
//     auto node = std::make_shared<NumberPublisherNode>();
//     rclcpp::spin(node);
//     rclcpp::shutdown();
//     return 0;
// } 

// to convert a node into a componenet
// remove the main function
// in the node class change the class constructor from:
//NumberPublisherNode() : Node("number_publisher")
//to::
// NumberPublisherNode(const rclcpp::NodeOptions &options) : Node("number_publisher", options)
// now include rclcpp componenets in heress
//put the entire node class into a namespace with package name a s the namespace name
// now register the node below heress
// and update cmakelistS.tXT and pakage.xml
// now build and source the package
// verify the node name "components_cpp::NumberPublisher)" in terminal with -> "ros2 component types"
// now load the component container manager
// "ros2 run rclcpp_components component_container"
// now run the component node that we created
// 'ros2 component load /ComponentManager components_cpp components_cpp::NumberPublisher'
// loading and unloading a ROS2 component
// to unload
// verify the component id
//ros2 component list
/*
/ComponentManager
  2  /number_publisher  -> node id
  */
// now unload using the component id
//' ros2 component unload /ComponentManager 2' -> id is 2
// to load again
//'ros2 component load /ComponentManager components_cpp components_cpp::NumberPublisher'
// we can rename the node runtime
//'ros2 component load /ComponentManager components_cpp components_cpp::NumberPublisher -r__node:=abdSSS'
// we can run a component without a container using standalone
// 'ros2 component standalone components_cpp components_cpp::NumberPublisher'
// there are three types of component executors
//'ros2 run rclcpp_components <tab>'
/*
component_container   -> single threadded
component_container_isolated  -> each node will be ran in each single threaded executor(used by nav2 stack)
component_container_mt  -> multi threadeds heress
*/





#include "rclcpp_components/register_node_macro.hpp"
RCLCPP_COMPONENTS_REGISTER_NODE(components_cpp::NumberPublisher);

