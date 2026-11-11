from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import os


def generate_launch_description():     #name of the function should be exactly this never change the name of the function

    ld = LaunchDescription()

    #param_file_configuration
    param_config = os.path.join(get_package_share_directory("my_robot_bringup"),
                                "config", "number_app.yaml")

    #param_config = os.path.join(get_package_share_directory("<launch_filess_package_directory_is_req>"),"<config_folder(usually---"config">)", "<yaml_file_parameter_file_in_config_folder>")
    
    #node 1
    number_publisher = Node(           #custom node_name
        package="my_robot_py_pkg",       #package="<rename_package_name>"
        executable="num_pub",              #executable="<execcutable_name"
        name="my_number_publisher",           #name="<change_node_name
        
        namespace="/abc",

        remappings=[("/number", "/my_number")]   #remappings=[{"current_topic_name_in_node_code", "<renamed_topic_name(custom_name)>"}]
    )
    #node 2
    number_counter = Node(
        package="my_robot_py_pkg",
        executable="num_count",
        name="my_number_counter",
        #name_space: (remember to remove ("/") in the topic remappings=[("/number", "/my_number")] to [("number", "my_number")])
        namespace="/abc",      #namespace="<custom_namespace_name>"
        remappings=[("/number", "/my_number")]
    )
    # node3
    number_publisher_params = Node(
        package="my_robot_py_pkg",
        executable="number_pub_param",
        #name="my_custom_number_pub_param",
        remappings= [("/number_top", "/number_btm")],
        # parameters= [{"number": 12},
        #              {"time_period": 1.8}]
        # TO Add pARAmeter file instead of individual parameters:
        # make sure you have imported above:
                #from ament_index_python.packages import get_package_share_directory
                #import os
                #param_filess_configuration
        parameters=[param_config]

    )

    ld.add_action(number_publisher)   #ld.add_action(<custom_node_name>)
    ld.add_action(number_counter)
    ld.add_action(number_publisher_params)



    



    return ld