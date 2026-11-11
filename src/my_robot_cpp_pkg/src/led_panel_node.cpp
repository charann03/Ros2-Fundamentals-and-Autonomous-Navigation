#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/led_panel_state.hpp"
#include "my_robot_interfaces/srv/set_led.hpp"
#include <vector>
#include <sstream>

using namespace std::chrono_literals;
using namespace std::placeholders;

class LedPanelNode : public rclcpp::Node // MODIFY NAME
{
public:
    LedPanelNode() : Node("LedPanelNode") // MODIFY NAME
    {
        //initiaalize the publisher
        publisher_ = this->create_publisher<my_robot_interfaces::msg::LedPanelState>("led_panel_state", 10);
        //initialize the timer
        timer_ = this->create_wall_timer(0.1s,std::bind(&LedPanelNode::led_states_callback, this));
        //initialize the service
        server_ = this->create_service<my_robot_interfaces::srv::SetLed>("set_led",std::bind(&LedPanelNode::set_led_callback, this, _1,_2));

        //log the node
        RCLCPP_INFO(this->get_logger(), "led panel node has started successfully!!!!!!");


    }


private:
    //declare the publisher
    rclcpp::Publisher<my_robot_interfaces::msg::LedPanelState>::SharedPtr publisher_;
    //declare the timer
    rclcpp::TimerBase::SharedPtr timer_;
    //declare the service
    rclcpp::Service<my_robot_interfaces::srv::SetLed>::SharedPtr server_;
    //initialize the variables
    std::vector<int64_t> ledstate = {0,0,0}; // the values inside the vector are of int64_t type
    // led states callback
    void led_states_callback(){

        auto msg_ = my_robot_interfaces::msg::LedPanelState();
        
        msg_.ledstate = ledstate;
        publisher_->publish(msg_);

    }
    // convert vector led_states into string
    std::string vectortostring(const std::vector<int64_t> &ledstates) const{
        std::stringstream ss;
        for(int64_t led_state : ledstates){
            ss << led_state <<' ';
        }
        return ss.str();
    }

    // set led callback
    void set_led_callback(const my_robot_interfaces::srv::SetLed::Request::SharedPtr request,
                          const my_robot_interfaces::srv::SetLed::Response::SharedPtr response){
        // auto msg_ = my_robot_interfaces::msg::LedPanelState();

        if (request->lednumber == 1 && request->state == "on"){
            ledstate[request->lednumber-1] = 1;
            // ledstate = {1,0,0};
            response->success = true;
            RCLCPP_INFO(this->get_logger(), "led_panel state updated to {%s} ", vectortostring(ledstate).c_str());

            // publisher_->publish(msg_);

        }
        else if (request->lednumber == 2 && request->state == "on"){
            ledstate[request->lednumber -1] = 1;
            response->success = true;
            RCLCPP_INFO(this->get_logger(), "led_panel state updated to {%s} ", vectortostring(ledstate).c_str());


            // publisher_->publish(msg_);

        }
        else if (request->lednumber == 3 && request->state == "on"){
            ledstate[request->lednumber-1] = 1;
            // ledstate = {0,0,1};
            response->success = true;
            RCLCPP_INFO(this->get_logger(), "led_panel state updated to {%s} ", vectortostring(ledstate).c_str());


            // publisher_->publish(msg_);

        }
        else if (request->lednumber == 1 && request->state == "off"){
            ledstate[request->lednumber-1] = 0;
            // ledstate = {1,0,0};
            response->success = true;
            RCLCPP_INFO(this->get_logger(), "led_panel state updated to {%s} ", vectortostring(ledstate).c_str());


            // publisher_->publish(msg_);

        }
        else if (request->lednumber == 2 && request->state == "off"){
            ledstate[request->lednumber -1] = 0;
            response->success = true;
            RCLCPP_INFO(this->get_logger(), "led_panel state updated to {%s} ", vectortostring(ledstate).c_str());


            // publisher_->publish(msg_);

        }
        else if (request->lednumber == 3 && request->state == "off"){
            ledstate[request->lednumber-1] = 0;
            // ledstate = {0,0,1};
            response->success = true;
            RCLCPP_INFO(this->get_logger(), "led_panel state updated to {%s} ", vectortostring(ledstate).c_str());


            // publisher_->publish(msg_);

        }
        else{
            response->success = false;
            RCLCPP_INFO(this->get_logger(), "invalid operation, aborted!!!");


        }
    }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LedPanelNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}