cmake_minimum_required(VERSION 3.8)
project(ros2_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(action_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Ex5FullMessage.msg"
  "msg/Ex5SkeletonMessage.msg"
  "srv/Ex5FullService.srv"
  "srv/Ex5SkeletonService.srv"
  "action/Ex5FullAction.action"
  "action/Ex5SkeletonAction.action"
  DEPENDENCIES action_msgs
)

# Install Python Module
# ament_python_install_package(${PROJECT_NAME})

# Install Python executables
install(PROGRAMS
  scripts/ex1_pub_sub/full_pub.py
  scripts/ex1_pub_sub/full_sub.py
  scripts/ex1_pub_sub/skeleton_pub.py
  scripts/ex1_pub_sub/skeleton_sub.py
  scripts/ex2_service/full_srv.py
  scripts/ex2_service/skeleton_srv.py
  scripts/ex3_action/full_action.py
  scripts/ex3_action/skeleton_action.py
  scripts/ex5_custom_msg/ex5_full_custom.py
  DESTINATION lib/${PROJECT_NAME}
)

################ INSTALL LAUNCH, ETC #################
install(DIRECTORY

  # config <<< put your directory name here
  # launch <<< put your directory name here
  # scripts <<< put your directory namehere
    config
    launch
    scripts


  DESTINATION share/${PROJECT_NAME})

ament_package()
