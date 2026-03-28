#!/usr/bin/env python3  
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

class TurtleTracker(Node):
    def __init__(self):
        super().__init__('turtle_tracker_node')
        # 1. สร้าง Subscriber เพื่อรับข้อมูลพิกัด
        self.subscription = self.create_subscription(
            Pose, '/turtle1/pose', self.pose_callback, 10)

    def pose_callback(self, msg):
        # 2. แสดงผลพิกัด X, Y แบบ Real-time
        self.get_logger().info(f'พิกัดปัจจุบัน -> X: {msg.x:.2f}, Y: {msg.y:.2f}')

def main():
    rclpy.init()
    rclpy.spin(TurtleTracker())
    rclpy.shutdown()

if __name__ == '__main__':
    main()