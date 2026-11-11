#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "my_robot_interfaces/action/count_until.hpp" 

// create a shortcut for my_robot_interfaces::action::CountUntil
using CountUntil = my_robot_interfaces::action::CountUntil;
//placeholder namespace for std::bind
using namespace std::placeholders;
// short cut for goal_handle
using CountUntilGoalHandle = rclcpp_action::ClientGoalHandle<CountUntil>;
// for giving time
using namespace std::chrono_literals;
// for goal status
using GoalResultCode = rclcpp_action::ResultCode;

class CountUntilClientNode : public rclcpp::Node // MODIFY NAME
{
public:
    CountUntilClientNode() : Node("CountUntilClientNode") // MODIFY NAME
    {
        count_until_Client_ = rclcpp_action::create_client<CountUntil>(
            this,
            "count_until"
        );

    }
    // client send goal
    void send_goal(int target_number, double period){
        while (!count_until_Client_->wait_for_action_server(1.0s)){
            RCLCPP_WARN(this->get_logger(), "waiting for Count Until Action Server");
        }
        //create a goal
        auto goal = CountUntil::Goal();
        goal.target_number = target_number;
        goal.period = period;
        // Add callback
        auto options = rclcpp_action::Client<CountUntil>::SendGoalOptions();
        //result callback is
        options.result_callback = std::bind(&CountUntilClientNode::goal_result_callback, this, _1);
        // feedback callback is
        options.feedback_callback = std::bind(&CountUntilClientNode::goal_feedback_callback, this, _1, _2);
        // goal response callback
        options.goal_response_callback = std::bind(&CountUntilClientNode::goal_response_callback, this,_1);
        //send the goal
        RCLCPP_INFO(this->get_logger(), "sendin goal to server is !!!!! ");
        count_until_Client_->async_send_goal(goal,options); //send the goal and the options for callback
        // mimic cancelling functionality
        // timer_ = this->create_wall_timer(3.6s, 
        //                                  std::bind(&CountUntilClientNode::cancel_goal, this));
    }


private:
    // create  a client pointer is here
    rclcpp_action::Client<CountUntil>::SharedPtr count_until_Client_;
    // create a dummy timer to mimic goal cancelling
    rclcpp::TimerBase::SharedPtr timer_;
    // create Goal handle pointer
    CountUntilGoalHandle::SharedPtr goal_handle_;
    // result callback function
    void goal_result_callback(const CountUntilGoalHandle::WrappedResult &result){
        // for result
        int reached_number = result.result->reached_number;
        RCLCPP_INFO(this->get_logger(), "result: %d", reached_number);
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
    //feedback callback function
    void goal_feedback_callback(const CountUntilGoalHandle::SharedPtr &goal_handle,
                       const std::shared_ptr<const CountUntil::Feedback> &feedback)
    {
        (void) goal_handle; // since nothing to do with me make it void
        int current_number = feedback->current_number;
        RCLCPP_INFO(this->get_logger(), "current_number is : %d",current_number);
    }
    // goal response callback
    void goal_response_callback(const CountUntilGoalHandle::SharedPtr &goal_handle){

        if (goal_handle != nullptr){ // if goal is accepted goal handle is not a null pointer
            // carry the goal handle for handling cancel requests
            this->goal_handle_ = goal_handle;
            RCLCPP_INFO(this->get_logger(), "Goal Accepted!!!!!!");
        }
        else{ // if goal handle becomes null pointer
            RCLCPP_FATAL(this->get_logger(), "Goal Rejected!!!!!!");
        }
    }
    // cancel a goal
    // void cancel_goal(const std::shared_ptr<CountUntilGoalHandle> goal_handle){
    //     RCLCPP_INFO(this->get_logger(), "cancelling the goal");
    //     count_until_Client_->async_cancel_goal(goal_handle);
    // }

//     void cancel_goal()
//   {
//     RCLCPP_INFO(get_logger(), "Requesting to cancel goal");
//     if (!goal_handle_) // if goal handle is a null pointer
//     {
//         RCLCPP_ERROR(get_logger(), "Goal handle is null");
//         return;
//     }
 
//     auto future = count_until_Client_->async_cancel_goal(goal_handle_);
 
//     if (rclcpp::spin_until_future_complete(this->get_node_base_interface(), future) !=
//         rclcpp::FutureReturnCode::SUCCESS)
//     {
//         RCLCPP_ERROR(get_logger(), "Failed to cancel goal");
//         return;
//     }
//     RCLCPP_INFO(get_logger(), "Goal cancellation request sent");
//   }

    void cancel_goal(){
        RCLCPP_INFO(this->get_logger(), "cancelling the goalss");
        count_until_Client_->async_cancel_goal(this->goal_handle_); // the goal handle we receive from the response callback
        timer_->cancel();
    }





};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CountUntilClientNode>(); // MODIFY NAME
    // send goal here
    node->send_goal(6, 1.2);
    node->send_goal(12, 1.2);

    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}