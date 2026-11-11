#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::placeholders;

class AddTwoIntsServerNode : public rclcpp::Node // MODIFY NAME
{
public:
    AddTwoIntsServerNode() : Node("AddTwoIntsServerNode") // MODIFY NAME
    {   //initialize service server
        server_ = this->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints",  //service name heress
                                                                            std::bind(&AddTwoIntsServerNode::callbackAddTwoInts, //callback functon
                                                                                        this, _1,_2 ));
        RCLCPP_INFO(this->get_logger(),"add two ints server node has started!!!!!!");
    }

private:
    //declare service 
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;
    //service callback
    //here not to return anything unlike python
    void callbackAddTwoInts(const example_interfaces::srv::AddTwoInts::Request::SharedPtr request,
                            const example_interfaces::srv::AddTwoInts::Response::SharedPtr response)
    {   // perform the service action
        response->sum = request->a + request->b;
        // log the output
        // RCLCPP_INFO(this->get_logger(),"%ld + %ld = %ld",request->a, request->b, response->sum);  // %ld denotes long digits
        //or to keep it as int
        RCLCPP_INFO(this->get_logger(),"%d + %d = %d",(int)request->a, (int)request->b, (int)response->sum);  // %ld denotes long digits


    }
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoIntsServerNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}

/*
TO TEST THE SERVER IN CLI
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 6, b: 3}"
*/