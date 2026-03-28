#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from turtlesim.action import RotateAbsolute

class TurtleSpinner(Node):
    def __init__(self):
        super().__init__('turtle_spinner_node')
        # 1. สร้าง Action Client
        self._action_client = ActionClient(self, RotateAbsolute, '/turtle1/rotate_absolute')

    def send_rotation_goal(self, theta):
        # 2. เตรียมเป้าหมาย
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = theta
        
        self.get_logger().info('กำลังส่งคำสั่งหมุนตัว...')
        # 3. ส่งคำสั่งพร้อมผูก Callback สำหรับรับ Feedback ระหว่างทาง
        self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)

    def feedback_callback(self, feedback_msg):
        # 4. พิมพ์สถานะระหว่างที่เต่ากำลังค่อยๆ หมุน
        remaining = feedback_msg.feedback.remaining
        self.get_logger().info(f'เหลืออีก {remaining:.2f} เรเดียน จะถึงเป้าหมาย')

def main():
    rclpy.init()
    node = TurtleSpinner()
    node.send_rotation_goal(3.14) # หมุนไป 180 องศา
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()