#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute

class TurtleTeleporter(Node):
    def __init__(self):
        super().__init__('turtle_teleport_node')
        # TODO 1: สร้าง Service Client ไปที่ '/turtle1/teleport_absolute'
        
    def warp_turtle(self, x, y):
        # TODO 2: สร้าง Request และใส่ค่าเป้าหมาย
        
        # TODO 3: ส่งคำขอ (Call) ไปที่ Server
        pass

def main():
    rclpy.init()
    node = TurtleTeleporter()
    # TODO 4: เรียกฟังก์ชัน warp_turtle ไปที่ X=2.0, Y=2.0
    
    rclpy.spin_once(node) # รอรับผลลัพธ์ 1 ครั้ง
    rclpy.shutdown()

if __name__ == '__main__':
    main()