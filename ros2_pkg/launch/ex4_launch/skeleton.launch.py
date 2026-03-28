import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # TODO 1: สร้างและเรียกใช้ Node สำหรับ 'turtlesim_node' จากแพ็กเกจ 'turtlesim'
        # Node(
        #     package='...',
        #     executable='...',
        #     name='...'
        # ),

        # TODO 2: สร้างและเรียกใช้ Node สำหรับ 'full_pub.py' (หรือไฟล์ใดก็ได้) จากแพ็กเกจ 'ros2_pkg' ของเรา
        # Node(
        #     package='...',
        #     executable='...',
        #     name='...'
        # )
    ])
