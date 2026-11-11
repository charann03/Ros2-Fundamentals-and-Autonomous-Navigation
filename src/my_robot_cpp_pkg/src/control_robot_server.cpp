#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "my_robot_interfaces/action/control_robot.hpp"
#include <mutex>

// create a shortcut for my_robot_interfaces::action::CountUntil
using ControlRobot = my_robot_interfaces::action::ControlRobot;
//placeholder namespace for std::bind
using namespace std::placeholders;
// short cut for goal_handle
using ControlRobotGoalHandle = rclcpp_action::ServerGoalHandle<ControlRobot>;
// for time delay
using namespace std::chrono_literals;



class ControlRobotServerNode : public rclcpp::Node // MODIFY NAME
{
public:
    ControlRobotServerNode() : Node("ControlRobotServerNode") // MODIFY NAME
    {
        // initialize callback group for cancelling the goal
        cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
        // initialize action server in this heress
        this->control_robot_server_ = rclcpp_action::create_server<ControlRobot>(
            this,
            //name of action
            "control_robot",
            // goal callback
            std::bind(&ControlRobotServerNode::goal_callback, this, _1, _2),
            // cancel callback
            std::bind(&ControlRobotServerNode::cancel_goal_callback, this, _1),
            // handle accepted callback
            std::bind(&ControlRobotServerNode::handle_accepted_callback, this, _1),
            rcl_action_server_get_default_options(),
            // calback group for multi threadin heresg
            this->cb_group_





        );
        RCLCPP_INFO(this->get_logger(), "control robot server has started heress!!!!!!");
    }

private:
    // // Create object for mutex for goal_lock_
    std::mutex mutex_;
    // create an object of the goal UUID to (PREEMPT the Goal)
    rclcpp_action::GoalUUID preempted_goal_id_;
    // create a shared ptr to goal_handle in heress for goal policy
    std::shared_ptr<ControlRobotGoalHandle> goal_handle_;
    //declare action server
    rclcpp_action::Server<ControlRobot>::SharedPtr control_robot_server_;
    // create a callback group to enable multi threading for cancelling
    rclcpp::CallbackGroup::SharedPtr cb_group_;


    // goal callback function
    rclcpp_action::GoalResponse goal_callback(
        const rclcpp_action::GoalUUID &uuid,
        std::shared_ptr<const ControlRobot::Goal> goal
    )
    {
            (void) uuid;// (unused parameter)
            RCLCPP_INFO(this->get_logger(), "received a goal!!");
            if (goal->position <= 0 || goal->velocity <= 0){
                RCLCPP_WARN(this->get_logger(), "position or velocity cant be a negative or zero, rejectiong goal!!!!!!");
                return rclcpp_action::GoalResponse::REJECT;
            }

            // else accept the goal in heress
            RCLCPP_INFO(this->get_logger(), "accepting the goal!!");
            return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;

    }

    // cancel goal callback
    rclcpp_action::CancelResponse cancel_goal_callback(
        const std::shared_ptr<ControlRobotGoalHandle> goal_handle
    )
    {
        RCLCPP_INFO(this->get_logger(), "received a cancel reques in heress!!!!!!");
        (void) goal_handle; // since goal handle is not used
        return rclcpp_action::CancelResponse::ACCEPT;
    }
    // handle accepted callback
    void handle_accepted_callback(const std::shared_ptr<ControlRobotGoalHandle> goal_handle)
    {
        // goal policy - Preempting terminating previous goal and running the current goal
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        {
            // goal lockkk
            std::lock_guard<std::mutex> goal_lock_(mutex_);
            if (this->goal_handle_ && this->goal_handle_->is_active())
            {
                // auto goal_id = this->goal_handle_->get_goal_id();
                // to view a goal uuid we have to hash it and use a "%zu" format specifier since the goal uuid is of type size_t not int
                std::hash<rclcpp_action::GoalUUID> goal_id;
                RCLCPP_WARN(this->get_logger(), "Aborting current goal and ACCEPTING New GoalSS!!!!!! preempted goal id: %zu", goal_id(this->goal_handle_->get_goal_id()));
                preempted_goal_id_ = this->goal_handle_->get_goal_id();

            }

        }
        // execute goal heress
        execute_goal(goal_handle);
    }

    void execute_goal(const std::shared_ptr<ControlRobotGoalHandle> goal_handle)
    {   
        // create a goal hande pointer of the goal for preemption
        {
            std::lock_guard<std::mutex> goal_lock_(mutex_);
            goal_handle_ = goal_handle;
        }

        // explicitly giv ethe starting posnss
        int starting_position = 50;
        // get request from goal in heress
        int position = goal_handle->get_goal()->position;
        int velocity = goal_handle->get_goal()->velocity;

        //feedback
        auto feedback = std::make_shared<ControlRobot::Feedback>();
        // result
        auto result = std::make_shared<ControlRobot::Result>();
        // sleep to mimic 1s per meter
        rclcpp::Rate loop_rate(1s);
        // drive the robot
        int current_position = starting_position;
        while (current_position<position)
        {
            
            // #check if the goal cancel request is raised or wot
            if (goal_handle->is_canceling()){
                RCLCPP_INFO(this->get_logger(), "cancelling the goal in here isS!!!!!!");
                result->reached_position = current_position;
                result->message = "goal has cancel requested in heress";
                goal_handle->canceled(result);
                // must return here else the remaining code would be executed
                return;

            }

        // abort the preempted goal id here (actual termination is heress!!!!!!)
        {
            std::lock_guard<std::mutex> goal_lock_(mutex_);
            if (goal_handle->get_goal_id() == this->preempted_goal_id_){
                result->reached_position = current_position;
                result->message = "received new goal aborting old goalss!!!!!!";
                goal_handle->abort(result);
                return; // never forget to return
            }
        }

            // move the robot by velocity
            if((position - current_position)<velocity){
                current_position += (position - current_position);
            }
            else{
                current_position += velocity;
            }
            // publish feedback heress
            feedback->current_position = current_position;
            goal_handle->publish_feedback(feedback);
            RCLCPP_INFO(this->get_logger(), "current_position of robots is: %d", current_position);
            // mimic m/s
            loop_rate.sleep();


        }

        // return the result pointer into the goalhandle 
        if (position == current_position){ 
        // set final state and return result
        result->reached_position = current_position;
        result->message = "robot reached goalss ";
        goal_handle->succeed(result);
        RCLCPP_INFO(this->get_logger(), "Goal Succeeded!!!!!!");
        return;
    }
        else{
            result->reached_position = current_position;
            result->message = "robot goal failed aborted ";

            goal_handle->abort(result);
            RCLCPP_FATAL(this->get_logger(), "Goal Failed!!!!!!");
            return;

        }
        

    }

};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<ControlRobotServerNode>(); // MODIFY NAME
    auto executor = rclcpp::executors::MultiThreadedExecutor();
    executor.add_node(node);
    executor.spin();
    // rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}