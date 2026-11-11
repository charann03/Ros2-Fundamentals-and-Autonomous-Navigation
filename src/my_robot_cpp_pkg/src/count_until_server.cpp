#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "my_robot_interfaces/action/count_until.hpp" // look at .vscode -> c_cpp_properties.json and update the include path
#include <mutex>
#include <queue>



// create a shortcut for my_robot_interfaces::action::CountUntil
using CountUntil = my_robot_interfaces::action::CountUntil;
//placeholder namespace for std::bind
using namespace std::placeholders;
// short cut for goal_handle
using CountUntilGoalHandle = rclcpp_action::ServerGoalHandle<CountUntil>;
// for time delay
using namespace std::chrono_literals;



class CountUntilServerNode : public rclcpp::Node // MODIFY NAME
{
public:
    CountUntilServerNode() : Node("CountUntilServerNode") // MODIFY NAME
    {   
        // initialize callback group for cancelling the goal
        cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);

        // initialize action server
        count_until_server_ = rclcpp_action::create_server<CountUntil>(
            this,
            // name of ACTION
            "count_until",
            // goal_callback
            std::bind(&CountUntilServerNode::goal_callback, this, _1, _2),
            // cancel callback
            std::bind(&CountUntilServerNode::cancel_callback, this, _1),
            // handle accepted callback
            std::bind(&CountUntilServerNode::handle_accepted_callback, this, _1),
            // use default actionoptions
            rcl_action_server_get_default_options(),
            // callback groups heress
            this->cb_group_
            

        );
        RCLCPP_INFO(this->get_logger(), "Action Server has been STARTED!!!!!!!");

    }

private:

    // // Create object for mutex for goal_lock_
    std::mutex mutex_;
    // create an object of the goal UUID to (PREEMPT the Goal)
    rclcpp_action::GoalUUID preempted_goal_id_;
    rclcpp_action::Server<CountUntil>::SharedPtr count_until_server_;
    // create a callback group to enable multi threading for cancelling
    rclcpp::CallbackGroup::SharedPtr cb_group_;
    // create a shared ptr to goal_handle in heress for goal policy
    std::shared_ptr<CountUntilGoalHandle> goal_handle_;
    // goal callback function
    rclcpp_action::GoalResponse goal_callback(
        const rclcpp_action::GoalUUID &uuid, 
        std::shared_ptr<const CountUntil::Goal> goal){
            //since we do not use the goal and uuid params we make them void type
            (void) uuid;
            // (void) goal; //comment if goal is utilized for conditions
            RCLCPP_INFO(this->get_logger(), "received a goal!!");
            // POLICY- REJECT NEW GOAL WHEN OLD GOAL IS RUNNING
            //---------------------------------------------------------------------------
                // {
                //     std::lock_guard<std::mutex> goal_lock_(mutex_);
                //     if (  this->goal_handle_ && this->goal_handle_->is_active()){
                //         RCLCPP_WARN(this->get_logger(), "A goal still active rejecting new goalss!!!!!!");
                //         return rclcpp_action::GoalResponse::REJECT;
                //     }
                // }
            //---------------------------------------------------------------------------
        

            if (goal->target_number <= 0.0){
                RCLCPP_FATAL(this->get_logger(),"Negative number is,Rejecting thae Goal!!");
                return rclcpp_action::GoalResponse::REJECT;
            }
             // if not accept the goal heress   
            RCLCPP_INFO(this->get_logger(),"Accepting thae Goal!!");

            return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
        }

    // cancel callback function
    rclcpp_action::CancelResponse cancel_callback(const std::shared_ptr<CountUntilGoalHandle> goal_handle){
        RCLCPP_INFO(this->get_logger(), "received a cancel reques in heress!!!!!!");
        (void) goal_handle; // since goal handle is not used
        return rclcpp_action::CancelResponse::ACCEPT;
    }
    // handle accepted callback() to execute the goal

    void handle_accepted_callback(const std::shared_ptr<CountUntilGoalHandle> goal_handle){
                // RCLCPP_INFO(this->get_logger(), "inside condition heress");

        // goal policy - Preempting terminating previous goal and running the current goal
        // ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        // {
        //     // goal lockkk
        //     std::lock_guard<std::mutex> goal_lock_(mutex_);
        //     if (this->goal_handle_ && this->goal_handle_->is_active())
        //     {
        //         // auto goal_id = this->goal_handle_->get_goal_id();
        //         // to view a goal uuid we have to hash it and use a "%zu" format specifier since the goal uuid is of type size_t not int
        //         std::hash<rclcpp_action::GoalUUID> goal_id;
        //         RCLCPP_WARN(this->get_logger(), "Aborting current goal and ACCEPTING New GoalSS!!!!!! preempted goal id: %zu", goal_id(this->goal_handle_->get_goal_id()));
        //         preempted_goal_id_ = this->goal_handle_->get_goal_id();

        //     }

        // }
                // execute the accepted goal
                execute_goal(goal_handle);
        //-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
                // RCLCPP_INFO(this->get_logger(), "inside condition heress");

    }

    // execute callback function
    void execute_goal(const std::shared_ptr<CountUntilGoalHandle> goal_handle){
        // create a scope to mimic with goal_lock_ in python
        {
            std::lock_guard<std::mutex> goal_lock_(mutex_);
            // make the goal_handle_explicit for goal policy
            this->goal_handle_ = goal_handle;
        }

        // action functionality code in here sss
        // get request from goal
        int target_number = goal_handle->get_goal()->target_number;
        double period = goal_handle->get_goal()->period;

        // feedback
        auto feedback = std::make_shared<CountUntil::Feedback>();
        // result
        auto result = std::make_shared<CountUntil::Result>();
        //initialize the counter
        int counter = 0;
        // for sleeping
        rclcpp::Rate loop_rate(1.0/period);
        // delay to prevent missing out feedbak data
        std::this_thread::sleep_for(0.05s);  // delay for 50milliseconds
        for (int i =0 ; i<target_number; i++){

            // #check if the goal cancel request is raised or wot
            if (goal_handle->is_canceling()){
                RCLCPP_INFO(this->get_logger(), "cancelling the goal in here isS!!!!!!");
                result->reached_number = counter;
                goal_handle->canceled(result);
                // must return here else the remaining code would be executed
                return;

            }
        //     abort the preempted goal id here (actual termination is heress!!!!!!)
        // {
        //     std::lock_guard<std::mutex> goal_lock_(mutex_);
        //     if (goal_handle->get_goal_id() == this->preempted_goal_id_){
        //         result->reached_number = counter;
        //         goal_handle->abort(result);
        //         return; // never forget to return
        //     }
        // }
            //inc the counter
            counter++ ;

            // to publish feedback
            feedback->current_number = counter;
            goal_handle->publish_feedback(feedback);
            RCLCPP_INFO(this->get_logger(), "current_number is: %d", counter);
            // sleep
            loop_rate.sleep();
            

        }
        // set final state and return result
        result->reached_number = counter;
        // return the result pointer into the goalhandle 
        if (target_number == counter){ 
        goal_handle->succeed(result);
        RCLCPP_INFO(this->get_logger(), "Goal Succeeded!!!!!!");
    }
        else{
            RCLCPP_FATAL(this->get_logger(), "Goal Failed!!!!!!");

        }
    }



    
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<CountUntilServerNode>(); // MODIFY NAME
    // create a executor for multi threading
    auto executor = rclcpp::executors::MultiThreadedExecutor();
    executor.add_node(node);
    executor.spin();
    // rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}





