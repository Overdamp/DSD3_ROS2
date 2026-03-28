#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleMover(Node):
    def __init__(self):
        super().__init__('turtle_mover_node')
        # 1. สร้าง Publisher
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        # 2. สร้าง Timer
        self.timer = self.create_timer(0.5, self.move_turtle)

    def move_turtle(self):
        msg = Twist()
        # 3. กำหนดให้เต่าวิ่งเป็นวงกลม (เดินหน้า 2.0, เลี้ยว 1.8)
        msg.linear.x = 2.0
        msg.angular.z = 1.8
        # 4. ส่งคำสั่ง
        self.publisher_.publish(msg)
        self.get_logger().info('กำลังสั่งเต่าวิ่งเป็นวงกลม...')

def main():
    rclpy.init()
    node = TurtleMover()
    rclpy.spin(node) # 5. รันค้างไว้
    rclpy.shutdown()

if __name__ == '__main__':
    main()