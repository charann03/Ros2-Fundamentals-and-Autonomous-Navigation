#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"
// simplify timers
using namespace std::chrono_literals;

class RobotNewsPublisherNode : public rclcpp::Node // MODIFY NAME
{
public:
    RobotNewsPublisherNode() : Node("Robot_News_Publisher_Node") , robot_name_("arthur") // MODIFY NAME
    {
        //initialize the publisher
        publisher_ = this->create_publisher<example_interfaces::msg::String>("robot_news", 10); // topic name , qos
        //initialize the timer
        timer_ = this->create_wall_timer(0.5s, //cllback every 0.5second (due to chrono_literals)
                                    std::bind(&RobotNewsPublisherNode::publishNews, //Function Mynode::timerCallback
                                    this));   
        RCLCPP_INFO(this->get_logger(), "robot news has been started in here!!!!!!");
    }

private:
    //declare the publisher
    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    //declare robot_name
    std::string robot_name_;
    //declare the timer
    rclcpp::TimerBase::SharedPtr timer_;


    // publisher function and timer callback
    void publishNews(){
        auto msg = example_interfaces::msg::String();
        msg.data = "robot news is published by robot: "+ robot_name_ + " from the robot news station...";
        publisher_->publish(msg);  // ie (*publisher_).publish(msg)
        
    }   



};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RobotNewsPublisherNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}