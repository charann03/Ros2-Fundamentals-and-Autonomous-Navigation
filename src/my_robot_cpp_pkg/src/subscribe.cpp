#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

using namespace std::placeholders;

class Charan : public rclcpp::Node{
    public:
        Charan(): Node("Charan_robot"){
            subscribe_=this->create_subscription<example_interfaces::msg::String>("ramkumar",10,std::bind(&Charan::sub_cb, this,_1 ));
        }
    private:
        rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscribe_;

        void sub_cb(const example_interfaces::msg::String msg_){
            RCLCPP_INFO(this->get_logger(),"%s",msg_.data.c_str());
        }
};
int main(int argc,char **argv){
    rclcpp::init(argc,argv);
    auto node = std::make_shared<Charan>();
    rclcpp::spin(node);
    rclcpp::shutdown();
}