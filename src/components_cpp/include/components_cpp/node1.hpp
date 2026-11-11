// #pragma once
#include "rclcpp/rclcpp.hpp"
#include <chrono>
#include <thread>


using namespace std::chrono_literals;

class Node1 : public rclcpp::Node
{
public:
    Node1() : Node("node1")
    {
        cb_group = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
        this->timer1_ = this->create_wall_timer(1000ms, std::bind(&Node1::callbackTimer1, this)
        // , this->cb_group
    );
        this->timer2_ = this->create_wall_timer(1000ms, std::bind(&Node1::callbackTimer2, this)
        // , this->cb_group
    );
        this->timer3_ = this->create_wall_timer(1000ms, std::bind(&Node1::callbackTimer3, this)
        // ,this->cb_group
    );
    }

private:

    void callbackTimer1()
    {
        std::this_thread::sleep_for(2000ms);
        RCLCPP_INFO(this->get_logger(), "cb 1");
    }

    void callbackTimer2()
    {
        std::this_thread::sleep_for(2000ms);
        RCLCPP_INFO(this->get_logger(), "cb 2");
    }

    void callbackTimer3()
    {
        std::this_thread::sleep_for(2000ms);
        RCLCPP_INFO(this->get_logger(), "cb 3");
    }

    rclcpp::TimerBase::SharedPtr timer1_;
    rclcpp::TimerBase::SharedPtr timer2_;
    rclcpp::TimerBase::SharedPtr timer3_;
    rclcpp::CallbackGroup::SharedPtr cb_group;
};