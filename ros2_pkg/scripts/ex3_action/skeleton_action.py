#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class TurtleSpinner(Node):
    def __init__(self):
        super().__init__('turtle_spinner_node')
        # TODO 1: สร้าง Action Client 
        
    def send_rotation_goal(self, theta):
        # TODO 2: สร้าง Goal กำหนดมุม theta
        
        # TODO 3: ส่ง Goal ไปที่ Server และผูกฟังก์ชันรับ Feedback
        pass
        
    def feedback_callback(self, feedback_msg):
        # TODO 4: ปริ้นท์บอกระยะมุมที่เหลืออยู่ (remaining)
        pass

def main():
    rclpy.init()
    node = TurtleSpinner()
    # ส่งเป้าหมายให้หมุนไปที่มุม 3.14 (หันกลับหลัง 180 องศา)
    node.send_rotation_goal(3.14)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()