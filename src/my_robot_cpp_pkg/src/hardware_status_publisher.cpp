#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/hardware_status.hpp"
#include "my_robot_interfaces/srv/compute_rectangle_area.hpp"

using namespace std::chrono_literals;
using namespace std::placeholders;

class HardWareStatusNode : public rclcpp::Node // MODIFY NAME
{
public:
    HardWareStatusNode() : Node("HardWareStatusNode") // MODIFY NAME
    {   //initialize publisher
        publisher_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>("hw_status", 10);
        //initialize timer
        timer_ = this->create_wall_timer(1s, std::bind(&HardWareStatusNode::hw_status_callback, this));
        //initialize the service
        server_ = this->create_service<my_robot_interfaces::srv::ComputeRectangleArea>("compute_rectangle_area",
                                                                                        std::bind(&HardWareStatusNode::compute_rect_area_callback, this, _1,_2));


        // log the node hs started
        RCLCPP_INFO(this->get_logger(), "hardware status publisher node has started!!!!!!");


    }

private:
    //declare the publisher
    rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr publisher_;
    //declare the timer
    rclcpp::TimerBase::SharedPtr timer_;
    //declare service 
    rclcpp::Service<my_robot_interfaces::srv::ComputeRectangleArea>::SharedPtr server_;
    // HW_Status publisher callback
    const float IDEAL_TEMP = 36.00;
    const float MAX_TEMP  = 100.00;
    float current_temp = 36.00;


    void hw_status_callback(){

        auto msg_ = my_robot_interfaces::msg::HardwareStatus();
        if (current_temp >= IDEAL_TEMP && current_temp<= MAX_TEMP/2){
            msg_.temperature = current_temp;
            msg_.are_motors_ready = true;
            msg_.debug_message = "temperture is within threshold";
            publisher_->publish(msg_);
            current_temp ++;

        }
        else if(current_temp > MAX_TEMP/2 && current_temp < MAX_TEMP){
            msg_.temperature = current_temp;
            msg_.are_motors_ready = false;
            msg_.debug_message = "temperture is out of the threshold";
            publisher_->publish(msg_);
            current_temp ++;



        }
        else{
            msg_.temperature = current_temp;
            msg_.are_motors_ready = false;
            msg_.debug_message = "temperture is out of the threshold";
            publisher_->publish(msg_);
            current_temp = 36.0;
        }

    } 

    // compute_rect_areaaaaaaa callback function is
    void compute_rect_area_callback(const my_robot_interfaces::srv::ComputeRectangleArea::Request::SharedPtr request,
                                    const my_robot_interfaces::srv::ComputeRectangleArea::Response::SharedPtr response)
    {
        response->area = request->length * request->width;
        RCLCPP_INFO(this->get_logger(), "the area of length: %lf and width: %lf is : %lf meters.sq",request->length,request->width, response->area);
    }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardWareStatusNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}