#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/srv/set_led.hpp"

using namespace std::chrono_literals;

class BatteryNode : public rclcpp::Node // MODIFY NAME
{
public:
    BatteryNode() : Node("BatteryNode") // MODIFY NAME
    {
        //initialize the client
        client_ = this->create_client<my_robot_interfaces::srv::SetLed>("set_led");
    }
    //set led client call back

    void set_led_client(const int lednumber_, std::string state_){
        while(!client_->wait_for_service(1s)){
            RCLCPP_WARN(this->get_logger(), "waiting for set led service!!!!!!");
        }

        //set the led_number and status request
        auto request = std::make_shared<my_robot_interfaces::srv::SetLed::Request>();
        request->lednumber = lednumber_;
        request->state = state_;

        //send client request
        client_->async_send_request(request,[=](rclcpp::Client<my_robot_interfaces::srv::SetLed>::SharedFuture future){
            auto response = future.get();
            RCLCPP_INFO(this->get_logger(), "led number %d is set to \"%s\" state, operation status \"%s\"",(int)request->lednumber,(request->state).c_str(),((response->success)? "true" : "false"));
        });

            
        }
        void battery_mimic(){
            while(true){
            sleep(4); //battery dischare time
            RCLCPP_INFO(this->get_logger(),"battery is empty, powering on led!!!");
            this->set_led_client(3,"on");
            sleep(6); //charging the led
            this->set_led_client(3,"off");
            RCLCPP_INFO(this->get_logger(), "battery now charged, powering off led!!!");

        }
        }

private:
    //declare the client
    rclcpp::Client<my_robot_interfaces::srv::SetLed>::SharedPtr client_;
    
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<BatteryNode>(); // MODIFY NAME
    // node->set_led_client(1,"on");
    // sleep(3);
    // node->set_led_client(2,"on");
    // sleep(3);
    // node->set_led_client(3,"on");
    // sleep(3);
    // sleep(3);
    // node->set_led_client(2,"off");
    // sleep(3);
    // node->set_led_client(3,"off");
    // sleep(3);
    // node->set_led_client(1,"off");
    node->battery_mimic();



    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}