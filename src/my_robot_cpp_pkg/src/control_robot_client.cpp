#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "my_robot_interfaces/action/control_robot.hpp"
#include "example_interfaces/msg/empty.hpp"


// create a shortcut for my_robot_interfaces::action::CountUntil
using ControlRobot = my_robot_interfaces::action::ControlRobot;
//placeholder namespace for std::bind
using namespace std::placeholders;
// short cut for goal_handle
using ControlRobotGoalHandle = rclcpp_action::ClientGoalHandle<ControlRobot>;
// for time delay
using namespace std::chrono_literals;

// for goal status
using GoalResultCode = rclcpp_action::ResultCode;

class ControlRobotClientNode : public rclcpp::Node // MODIFY NAME
{
public:
    ControlRobotClientNode() : Node("ControlRobotClientNode") // MODIFY NAME
    {
        // initialize the action_client
        this->control_robot_client_ = rclcpp_action::create_client<ControlRobot>(
            this,
            "control_robot"

        );


        // initialize the cancel subscription in heress
        this->cancel_subscription_ = this->create_subscription<example_interfaces::msg::Empty>(
            "cancel_topic",
            1,
            std::bind(&ControlRobotClientNode::cancel_subcription_callback, this, _1)

        );

        RCLCPP_INFO(this->get_logger(), "control robot action client node has started!!!!!!");
    }


    // send_goal function heress
    void send_goal(const int position, const int velocity)
    {
        // waitss for server
        while (!control_robot_client_->wait_for_action_server(1.0s))
        {
            RCLCPP_WARN(this->get_logger(), "waiting for Count Until Action Server");
        }
        // create a goalss
        auto goal = ControlRobot::Goal();
        goal.position = position;
        goal.velocity = velocity;
        // add callback options
        auto options = rclcpp_action::Client<ControlRobot>::SendGoalOptions();
        //result callback is
        options.result_callback = std::bind(&ControlRobotClientNode::goal_result_callback, this, _1);
        // feedback callback is
        options.feedback_callback = std::bind(&ControlRobotClientNode::goal_feedback_callback, this, _1, _2);
        // goal response callback
        options.goal_response_callback = std::bind(&ControlRobotClientNode::goal_response_callback, this,_1);

        //send the goal
        RCLCPP_INFO(this->get_logger(), "sendin goal to server is !!!!! ");
        control_robot_client_->async_send_goal(goal,options); //send the goal and the options for callback


    }

private:
    // declare the action client
    rclcpp_action::Client<ControlRobot>::SharedPtr control_robot_client_;
    // create Goal handle pointer
    std::shared_ptr<ControlRobotGoalHandle> goal_handle_;
    // cancel goal subscription
    rclcpp::Subscription<example_interfaces::msg::Empty>::SharedPtr cancel_subscription_;
    
    
    
    // result callback function
    void goal_result_callback(const ControlRobotGoalHandle::WrappedResult &result)
    {
        // for result
        int reached_position = result.result->reached_position;
        std::string message = result.result->message;
        RCLCPP_INFO(this->get_logger(), "Robot had reached the goal position: %d", reached_position);
        RCLCPP_INFO(this->get_logger(),"goal_message: %s", message.c_str());
        //for result code
        auto result_code = result.code;
        if (result_code == GoalResultCode::SUCCEEDED){
            RCLCPP_INFO(this->get_logger(), "goal Succeeded");
        }
        else if (result_code == GoalResultCode::ABORTED){
            RCLCPP_FATAL(this->get_logger(), "goal AbORTED");
        }
        else if (result_code == GoalResultCode::CANCELED){
            RCLCPP_FATAL(this->get_logger(), "goal CANceLED");
        }
        else if (result_code == GoalResultCode::UNKNOWN){
            RCLCPP_WARN(this->get_logger(), "goal DestrROYED");
        }
    }

    // callback function subscription
    void cancel_subcription_callback(const example_interfaces::msg::Empty::SharedPtr msg) const
    {   // if  msg received cancel the goalss
        if(msg)
        {
        RCLCPP_INFO(this->get_logger(), "cancelling the goalss");
        control_robot_client_->async_cancel_goal(this->goal_handle_); // the goal handle we receive from the response callback
        }
    }

    //feedback callback function
    void goal_feedback_callback(const ControlRobotGoalHandle::SharedPtr &goal_handle,
                       const std::shared_ptr<const ControlRobot::Feedback> &feedback)
    {
        (void) goal_handle; // since nothing to do with me make it void
        int current_position = feedback->current_position;
        RCLCPP_INFO(this->get_logger(), "current_Position of the robot is: %d", current_position);
    }


    // goal response callback
    void goal_response_callback(const ControlRobotGoalHandle::SharedPtr &goal_handle){

        if (goal_handle != nullptr){ // if goal is accepted goal handle is not a null pointer
            // carry the goal handle for handling cancel requests
            this->goal_handle_ = goal_handle;
            RCLCPP_INFO(this->get_logger(), "Goal Accepted!!!!!!");
        }
        else{ // if goal handle becomes null pointer
            RCLCPP_FATAL(this->get_logger(), "Goal Rejected!!!!!!");
        }
    }




};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ControlRobotClientNode >(); // MODIFY NAME
    
    node->send_goal(116,7);
    node->send_goal(116,7);
    node->send_goal(116,7);


    rclcpp::spin(node);


    rclcpp::shutdown();
    return 0;
}