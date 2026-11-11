#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"
#include <sstream>

using namespace std::chrono_literals;

class RamKUMAR : public rclcpp::Node{
    public: 
        
        RamKUMAR() : Node("ramkumar_robot_node") , counts(0){
            publisher_ = this->create_publisher<example_interfaces::msg::String>("ramkumar", 10);
            timer_= this->create_wall_timer(1.5s, [this](){
                            auto msg = example_interfaces::msg::String();
                            std::stringstream ss;
                            counts++;
                            ss << "iam ramkumar count: " << counts ;
                            std::string log_entry = ss.str();
                            msg.data = log_entry;
                            this->publisher_->publish(msg);
            });

            

        }
    private:
        rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
        int counts;
        // auto publisher;
        // auto timer;

        // void pub_cb(){
        //     auto msg = example_interfaces::msg::String();
        //     msg.data = "iam ramkumar ceo of zoho robotics";
        //     this->publisher_->publish(msg);
            
        // }

};


int main(int argc , char **argv){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RamKUMAR>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;

}