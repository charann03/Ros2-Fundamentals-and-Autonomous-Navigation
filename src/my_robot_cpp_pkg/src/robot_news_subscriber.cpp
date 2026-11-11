#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

//we can use namespace for std::placeholders
// ie..
using namespace std::placeholders;

class SmartPhone : public rclcpp::Node // MODIFY NAME
{
public:
    SmartPhone() : Node("Robot_news_subscriber_node") // MODIFY NAME
    {
        subscriber_ = this->create_subscription<example_interfaces::msg::String>("robot_news", //topic name
                                                                                 10,  // qos
                                                                                 std::bind(&SmartPhone::callback, this, _1) // callback function , since we have one parameter in the callback function we have to enter std::placeholders::_1 in the std::bind function
                                                                                ); 
        RCLCPP_INFO(this->get_logger(), "robot news subscription node has started!!!!!!");
    }

private:
    //declare the subscriber
    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
    //subscription callback function
    void callback(const example_interfaces::msg::String::SharedPtr msg_){ // since the msg can never be changed we use const
        
        RCLCPP_INFO(this->get_logger(), "%s", msg_->data.c_str()); // convert into const char* type ie.. into c-style string(needed for ros2)




    }



};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<SmartPhone>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}