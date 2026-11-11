#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::chrono_literals;
using namespace std::placeholders;

class AddTwoIntsClientNode : public rclcpp::Node // MODIFY NAME
{
public:
    AddTwoIntsClientNode() : Node("AddTwoIntsClientNode")  //, a(0), b(0)  // MODIFY NAME
    {
        //initialize the service
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
    }


    // client function
    
    void call_add_two_ints(const int a, const int b){
        // this->a = a;
        // this->b = b ;

        while(!client_->wait_for_service(1s)){
            RCLCPP_WARN(this->get_logger(), "waiting for add two ints service!!!!!!");
        }
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a;
        request->b = b;

        // client_->async_send_request(request, 
        //     std::bind(&AddTwoIntsClientNode::callback_call_add_two_ints, this, _1));

        client_->async_send_request(request,
                                    [=](rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future){
                auto response = future.get();
                RCLCPP_INFO(this->get_logger(),"%d + %d = %d",(int)request->a, (int)request->b, (int)response->sum); 
        });


    }
private:
    //declare the integers
    // int a,b;
    //declare the client
    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
    // service future callback
    // void callback_call_add_two_ints(
    //     rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future // create a future of sharedfuture
    // ){
    //     auto response = future.get();
    //     RCLCPP_INFO(this->get_logger(),"%d + %d = %d",a, b, (int)response->sum); 

        
    // }



};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoIntsClientNode>(); // MODIFY NAME
    node->call_add_two_ints(6,3);
    node->call_add_two_ints(9,18);
    node->call_add_two_ints(118,121);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}