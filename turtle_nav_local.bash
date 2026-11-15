# Local turtlesim environment; source in every ROS terminal.
source /opt/ros/jazzy/setup.bash
source /home/h8987/ros2_ws/install/setup.bash
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_AUTOMATIC_DISCOVERY_RANGE=LOCALHOST
unset FASTRTPS_DEFAULT_PROFILES_FILE FASTDDS_DEFAULT_PROFILES_FILE FASTDDS_BUILTIN_TRANSPORTS
