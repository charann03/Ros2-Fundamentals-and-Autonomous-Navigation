#include "rclcpp/rclcpp.hpp"

class Mynode : public rclcpp::Node{
    public:
        Mynode() : Node("cpp_test_oops") , counter_(0){  //node name heree:
            RCLCPP_INFO(this->get_logger(), "hellos_worlds_here!!!!!!");
            timer_ = this->create_wall_timer(std::chrono::seconds(1), //cllback every 1second
                                                std::bind(&Mynode::timerCallback, //Function Mynode::timerCallback
                                                this));                           // object: this refers to MMynode

            // if we have parameters
            // std::bind(
            // &Mynode::calculate,
            // this,
            // std::placeholders::_1 // adding a placeholders
            // )
            
        }
    private:
        //timer
        void timerCallback(){
            RCLCPP_INFO(this->get_logger(), "hellos %d", counter_);
            counter_ ++;

        }
        rclcpp::TimerBase::SharedPtr timer_;
        int counter_;



};

int main(int argc, char **argv){
    rclcpp::init(argc,argv); // initialize ros2
    //function code here
    auto node = std::make_shared<Mynode>();  //create a shared pointer of rclcpp::node // this runs the constructor Mynode()

    rclcpp::spin(node); // spin the node until its interupted
    
    rclcpp::shutdown(); // shutdoun ros2 node
    return 0;
}