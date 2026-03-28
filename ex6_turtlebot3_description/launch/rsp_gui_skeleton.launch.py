import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('ex6_turtlebot3_description')
    
    # โหลดไฟล์ URDF แบบฝึกหัด
    urdf_file = os.path.join(pkg_dir, 'urdf', 'turtlebot3_skeleton.urdf')
    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()
        
    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'urdf_config.rviz')
    
    # TODO 1: เขียนสร้าง Node สำหรับเรียกใช้ 'robot_state_publisher'
    # อย่าลืมใส่พารามิเตอร์ parameters=[{'robot_description': robot_desc}]
    # rsp_node = Node(...)
    
    # TODO 2: เขียนสร้าง Node สำหรับเรียกใช้ 'joint_state_publisher_gui'
    # jsp_gui_node = Node(...)
    
    # TODO 3: เขียนสร้าง Node สำหรับเรียกใช้ 'rviz2' 
    # อย่าลืมส่งอาร์กิวเมนต์โหลดไฟล์คอนฟิก: arguments=['-d', rviz_config_file]
    # rviz_node = Node(...)

    return LaunchDescription([
        # TODO 4: นำตัวแปร Node ทั้ง 3 ตัวที่สร้างไว้ด้านบน มาใส่เปิดใช้งานในลิสต์นี้
        
    ])
