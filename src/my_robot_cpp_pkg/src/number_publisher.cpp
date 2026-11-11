#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"
#include "rcl_interfaces/msg/set_parameters_result.hpp"
#include <vector>

using namespace std::chrono_literals;
using namespace std::placeholders;


class NumberPublisherNode : public rclcpp::Node // MODIFY NAME
{
public:

    //parameters callback function
    rcl_interfaces::msg::SetParametersResult params_callback(
        const std::vector<rclcpp::Parameter> &parameters)
    {
        rcl_interfaces::msg::SetParametersResult result;
        result.successful = false;
        result.reason = "";

        // Here update class attributes, do some actions, etc.
        for (const auto &param: parameters)
    {
        if (param.get_name() == "number")
        {
            if (param.get_type() == rclcpp::ParameterType::PARAMETER_INTEGER)
            {
                if (param.as_int() >= 1 && param.as_int() < 1000) // if number is in the range of 1 t0 999
                {
                    number_ = param.as_int();
                    result.successful = true;
                }
            }
        }
        if (param.get_name() == "timer_period")
        {
            if (param.get_type() == rclcpp::ParameterType::PARAMETER_DOUBLE)
            {
                if (param.as_double() >= 0.1 && param.as_double() < 10.0) // if number is in the range of 0.1 t0 10.0
                {
                    timer_period_ = param.as_double();
                    timer_->cancel();
                    if (timer_->is_canceled()){
                        timer_ = this->create_wall_timer(std::chrono::duration<double>(timer_period_),[this](){  // n=NOTE: when timer callback function must not take  any arguments, if thats the case use std::bind
                        auto msg_ = example_interfaces::msg::Int64();
                        // this->number_++;  // can write number++
                        msg_.data = number_;
                        this->publisher_->publish(msg_);
                    });
                    }
                    result.successful = true;
                    
                }
            }
        }


    }
        return result;
    }
    NumberPublisherNode() : Node("NumberPublisherNode")// MODIFY NAME
    { 
        
        //declare parameter
        this->declare_parameter("number", 6);
        this->declare_parameter("timer_period", 1.0);
        //get the parameter
        number_ = this->get_parameter("number").as_int();
        timer_period_ = this->get_parameter("timer_period").as_double();
        // parameter callback enablesinruntimeparametermodification
        callback_handle_ = this->add_on_set_parameters_callback(std::bind(&NumberPublisherNode::params_callback, this, _1));
        //initialize publisher
        publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number", 10);
        //initialize timer
        timer_ = this->create_wall_timer(std::chrono::duration<double>(timer_period_),[this](){  // n=NOTE: when timer callback function must not take  any arguments, if thats the case use std::bind
            auto msg_ = example_interfaces::msg::Int64();
            // this->number_++;  // can write number++
            msg_.data = number_;
            this->publisher_->publish(msg_);


        });

        //log the node
        RCLCPP_INFO(this->get_logger(), "number publisher node has started now!!!");
    }


private:
    //declare publisher
    rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
    //declare timer
    rclcpp::TimerBase::SharedPtr timer_;
    // callback handle declaration
    OnSetParametersCallbackHandle::SharedPtr callback_handle_;
    //initialize number
    int number_;
    //initialize timer period
    double timer_period_;




};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberPublisherNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}


//to test code
/*ros2 run my_robot_cpp_pkg number_publisher --ros-args -p number:=69 -p timer_period:=0.5 -p use_sim_time:=true
*/
//to test params file
/*ros2 run my_robot_cpp_pkg number_publisher --ros-args -r __node:=number_publisher1 --params-file /home/charann-inc5751/ros2_ws/src/my_robot_cpp_pkg/params/number_publisher_params.yaml 
*/