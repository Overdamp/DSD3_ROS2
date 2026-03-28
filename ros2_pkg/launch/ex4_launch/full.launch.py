import launch
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        # 1. รัน Node ของ turtlesim ให้หน้าต่างซิมูเลเตอร์จอสีฟ้าขึ้นมา
        Node(
            package='turtlesim',
            executable='turtlesim_node',
            name='turtlesim_sim'
        ),
        
        # 2. รัน Node Publisher ที่เราเขียนไว้ (สั่งเต่าวิ่งเป็นวงกลม)
        Node(
            package='ros2_pkg',
            executable='full_pub.py',
            name='turtle_mover'
        )
    ])
