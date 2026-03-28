#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute

class TurtleTeleporter(Node):
    def __init__(self):
        super().__init__('turtle_teleport_node')
        # 1. สร้าง Client 
        self.cli = self.create_client(TeleportAbsolute, '/turtle1/teleport_absolute')

    def warp_turtle(self, x, y):
        # 2. เตรียม Request
        req = TeleportAbsolute.Request()
        req.x = x
        req.y = y
        req.theta = 0.0 # หันหน้าตรง
        
        # 3. ส่งคำขอไปหา Server แบบ Asynchronous
        self.get_logger().info('กำลังสั่งวาปเต่า...')
        self.cli.call_async(req)

def main():
    rclpy.init()
    node = TurtleTeleporter()
    node.warp_turtle(2.0, 2.0) # 4. สั่งวาปไปมุมซ้ายล่าง
    
    # รันแค่ชั่วคราวเพื่อส่งคำสั่ง Service ให้เสร็จ แล้วโปรแกรมจบการทำงาน
    rclpy.spin_once(node) 
    rclpy.shutdown()

if __name__ == '__main__':
    main()