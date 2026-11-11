// #include "rclcpp/rclcpp.hpp"

// class Mynode : public rclcpp::Node{
//     public:
//         Mynode() : Node("cpp_test_oops") //node name heree:
//         { 

//         }
//         private:


// };

// int main(int argc, char **argv){
//     rclcpp::init(argc,argv); // initialize ros2
//     //function code here
//     auto node = std::make_shared<Mynode>();  //create a shared pointer of rclcpp::node type where we can give the node name "cpp_test"

//     rclcpp::spin(node); // spin the node until its interupted
    
//     rclcpp::shutdown(); // shutdoun ros2 node
//     return 0;
// }


//copy this for deploying the template
#include "rclcpp/rclcpp.hpp"

class MyCustomNode : public rclcpp::Node // MODIFY NAME
{
public:
    MyCustomNode() : Node("node_name") // MODIFY NAME
    {
    }

private:
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyCustomNode>(); // MODIFY NAME
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}