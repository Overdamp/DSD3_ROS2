#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
# นำเข้า Message ชนิด Pose ของ turtlesim
from turtlesim.msg import Pose

class TurtleTracker(Node):
    def __init__(self):
        super().__init__('turtle_tracker_node')
        # TODO 1: สร้าง Subscriber ไปที่ Topic '/turtle1/pose'
        # อย่าลืมผูกกับฟังก์ชัน pose_callback
        
    def pose_callback(self, msg):
        # TODO 2: พิมพ์ค่า msg.x และ msg.y ออกมาทางหน้าจอ
        pass

def main():
    rclpy.init()
    node = TurtleTracker()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()