#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::chrono_literals;

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    //node name
    auto node = std::make_shared<rclcpp::Node>("add_two_ints_client_no_oop"); // MODIFY NAME
    auto client = node->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints"); // service name of the server heress

    while(!client->wait_for_service(1s)){
        RCLCPP_WARN(node->get_logger(), "waiting for add two ints server!!!!!!");
    }
    // create a shared pointer of request
    auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
    request->a = 6;
    request->b = 3;

    auto future = client->async_send_request(request); // send the service request
    //spin the node until response
    rclcpp::spin_until_future_complete(node, future);

    auto response = future.get();  // returns the shared pointer of the response
    RCLCPP_INFO(node->get_logger(),"%d + %d = %d",(int)request->a, (int)request->b, (int)response->sum); 


    // rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}