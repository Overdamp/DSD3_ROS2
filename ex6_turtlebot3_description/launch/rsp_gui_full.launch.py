import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # หาที่อยู่ของแพ็กเกจ ex6_turtlebot3_description
    pkg_dir = get_package_share_directory('ex6_turtlebot3_description')
    
    # โหลดไฟล์ URDF ตัวเต็ม
    urdf_file = os.path.join(pkg_dir, 'urdf', 'turtlebot3_full.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
        
    # โหลดไฟล์คอนฟิก RViz
    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'urdf_config.rviz')
    
    # 1. Robot State Publisher Node (เผยแพร่ TF ตามโครงสร้างใน URDF)
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )
    
    # 2. Joint State Publisher GUI Node (แสดงหน้าต่างเลื่อนปรับองศา Joint)
    jsp_gui_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        output='screen'
    )
    
    # 3. RViz2 Node (แสดงหุ่น 3D)
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )

    return LaunchDescription([
        rsp_node,
        jsp_gui_node,
        rviz_node
    ])
