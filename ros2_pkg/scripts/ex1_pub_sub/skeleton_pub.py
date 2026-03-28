#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleMover(Node):
    def __init__(self):
        super().__init__('turtle_mover_node')
        # TODO 1: สร้าง Publisher ไปที่ Topic '/turtle1/cmd_vel'
        
        # TODO 2: สร้าง Timer ให้ทำงานทุก 0.5 วินาที เรียกฟังก์ชัน move_turtle
        
    def move_turtle(self):
        msg = Twist()
        # TODO 3: กำหนดความเร็วเชิงเส้น (linear.x) และความเร็วเชิงมุม (angular.z)
        
        # TODO 4: สั่ง Publish ข้อความ
        pass

def main():
    rclpy.init()
    # TODO 5: สร้างออบเจกต์และรัน spin
    rclpy.shutdown()

if __name__ == '__main__':
    main()