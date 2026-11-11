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
    {   // put the run goal queue thread function in the thread
        goal_queue_thread_ = std::thread(&CountUntilServerNode::run_goal_queue_thread, this);
        // initialize callback group for cancelling the goal
        cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::Reentrant);
        // create options to implement the callback group

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
    // join the goal queue thread to prevent memory LLeaks
    ~CountUntilServerNode()
    {
        goal_queue_thread_.join();
    }

private:
    // create a new to thread to execute the appended goals in the queue
    std::thread goal_queue_thread_;
    // create a list to to hold queued goal handles GOAL POLICY- queue goals heress
    std::queue<std::shared_ptr<CountUntilGoalHandle>> goal_queue_ = {};
    // // Create object for mutex for goal_lock_
    std::mutex mutex_;
    // action server poinyter
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
            // reject goal if negative target number
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
            
        //-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        // GOAL POLICY ___ QUEUE GOALSS
        //-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
            {   
                // locking to protect the goal_queue
                std::lock_guard<std::mutex> goal_lock_(mutex_);
                this->goal_queue_.push(goal_handle);
                RCLCPP_INFO(this->get_logger(), "added new goal to the queue!!!!!!! cutrrent queue size: %d", (int) goal_queue_.size());


            }
        //-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    }
    // runs the goals in the goal queue 
    void run_goal_queue_thread(){
        // slow_DOWn the thread to prevent highss cpu usage
        rclcpp::Rate loop_rate(1000.0); // 1000hz ie.,,, 1000 cycles per sec here we initializ ethe timer
        // create an infinite loop ie Keep this thread alive while ROS 2 is running.
        while(rclcpp::ok()){
            // create a pointer of the new goal handles
            std::shared_ptr<CountUntilGoalHandle> next_goal;
            {
            // goal lock to protect the goal queues
            std::lock_guard<std::mutex> goal_lock_(mutex_);
            // if the goal queue is not empty
            if(!goal_queue_.empty()){
                // assign the new goal and pop it 
                next_goal = goal_queue_.front();
                goal_queue_.pop();
            }
        }   
        // if goal is defined then execute it
            if (next_goal){
                RCLCPP_INFO(this->get_logger(), "Executing next goal in the queuess");
                execute_goal(next_goal);
            }
            loop_rate.sleep(); // 1000 cycles per sec

        }


    }

    // execute callback function
    void execute_goal(const std::shared_ptr<CountUntilGoalHandle> goal_handle){

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





