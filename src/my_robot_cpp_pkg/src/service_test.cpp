#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"
#include <sstream>


using namespace std::placeholders;
class ramservice : public rclcpp::Node // MODIFY NAME
{
public:
    ramservice() : Node("ramservice") // MODIFY NAME
    {
        service_ = this->create_service<example_interfaces::srv::AddTwoInts>("ramkumarservice",std::bind(&ramservice::service_callback, this, _1,_2));

    }

private:
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr service_;

    void service_callback(const example_interfaces::srv::AddTwoInts::Request::SharedPtr request, 
                          const example_interfaces::srv::AddTwoInts::Response::SharedPtr response){
        response->sum = request->a + request->b;
        std::stringstream ss;
        ss << request->a << " + " << request->b << " = " << response->sum;
        std::string srv_msg = ss.str(); 
        // RCLCPP_INFO(this->get_logger(),"%d + %d = %d", (int)request->a, (int)request->b, (int)response->sum);
        RCLCPP_INFO(this->get_logger(), "%s", srv_msg.c_str());
                          }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ramservice>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}