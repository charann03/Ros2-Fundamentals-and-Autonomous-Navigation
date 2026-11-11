from setuptools import find_packages, setup

package_name = 'my_robot_py_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='charann-inc5751',
    maintainer_email='charann-inc5751@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "py_node = my_robot_py_pkg.my_first_node:main",
            "oop_nodess = my_robot_py_pkg.my_oop_node:main",
            "rob_pub = my_robot_py_pkg.robot_publisher:main",
            "rob_sub = my_robot_py_pkg.robot_subscriber:main",
            "num_pub = my_robot_py_pkg.number_publisher:main",
            "num_count = my_robot_py_pkg.number_counter:main",
            "add_two_ints_server = my_robot_py_pkg.add_two_ints_server:main",
            "add_two_ints_client = my_robot_py_pkg.add_two_ints_client:main",
            "add_two_ints_client_no_oop = my_robot_py_pkg.add_two_ints_client_no_oop:main",
            "hw_statuss_pub = my_robot_py_pkg.hardware_status_publisher:main",
            "Led_panel = my_robot_py_pkg.led_panel_pub_server:main",
            "battery_state = my_robot_py_pkg.battery_client:main",
            "number_pub_param = my_robot_py_pkg.number_publisher_param:main",
            "Count_until_action_server = my_robot_py_pkg.count_until_server:main",
            "Count_until_action_client = my_robot_py_pkg.count_until_client:main",
            "robot_news = my_robot_py_pkg.robot_news_station:main",
            "smartPhone_sub = my_robot_py_pkg.smart_phone:main",
            "tas_two = my_robot_py_pkg.tortoisebot_t2_laser_dist:main",
            "tas_three = my_robot_py_pkg.tortoisebot_t3_ball_follow:main",
            "tas_five_one = my_robot_py_pkg.scan_to_cloud_t5_node:main",
            "tas_five_two = my_robot_py_pkg.fusion_t5:main",
            "pcl2_to_pcl = my_robot_py_pkg.pcl2_to_pcl:main",
            "waypoint_ntp = my_robot_py_pkg.waypoint_t7:main",
            "test_wp = my_robot_py_pkg.test_t7:main",
            "control_robot_server = my_robot_py_pkg.control_robot_server:main",
            "control_robot_client = my_robot_py_pkg.control_robot_client:main",
            "sub_pub_ack = my_robot_py_pkg.sub_pub_ack:main"


        
        ],
    },
)
