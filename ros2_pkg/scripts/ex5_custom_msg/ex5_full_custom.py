#!/usr/bin/env python3
import time
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

# ดึง Custom Interfaces ทั้ง 3 ข้อความ ที่เราสร้างไว้ในโฟลเดอร์ msg, srv, action
from ros2_pkg.msg import Ex5FullMessage
from ros2_pkg.srv import Ex5FullService
from ros2_pkg.action import Ex5FullAction

# นำเข้า Twist เพื่อเตรียมเอาไปขับเคลื่อนเต่า
from geometry_msgs.msg import Twist

class CustomAllInOneNode(Node):
    def __init__(self):
        super().__init__('ex5_full_custom_node')
        
        # Publisher เอาไว้ส่งแรงเพื่อควบคุมหุ่นจำลอง turtlesim
        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        
        # 1. Custom Topic Publisher (บรอดแคสต์สถานะตัวเองออกไปทุก 2 วินาที ด้วย Ex5FullMessage)
        self.status_pub = self.create_publisher(Ex5FullMessage, '/robot_info', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.counter = 0

        # 2. Custom Service Server (รอรับค่ากว้าง*ยาว ของ Ex5FullService มาคำนวณ แล้วสั่งเต่าเด้งเดินหน้าตามพื้นที่)
        self.srv = self.create_service(
            Ex5FullService, 
            '/custom_move', 
            self.service_callback
        )

        # 3. Custom Action Server (รอรับเลข target_count สั่งให้นับถอยหลังเป็นวินาที พร้อมกับให้เต่าหมุนตัว)
        self.action_server = ActionServer(
            self,
            Ex5FullAction,
            '/custom_countdown',
            self.action_execute_callback,
            # ใช้ ReentrantCallbackGroup เพื่ออนุญาตให้ Timer วิ่งไปได้เรื่อยๆ ในขณะที่เต่ากำลังค้างหมุนถอยหลังอยู่
            callback_group=ReentrantCallbackGroup()
        )
        self.get_logger().info("🔥 โหนด EX5 All-in-One (Custom Interfaces) พร้อมทำงานแล้ว!")
        self.get_logger().info("💡 ลองเทส Topic: ros2 topic echo /robot_info")
        self.get_logger().info('💡 ลองเทส Service: ros2 service call /custom_move ros2_pkg/srv/Ex5FullService "{width: 2.0, length: 1.5}"')
        self.get_logger().info('💡 ลองเทส Action: ros2 action send_goal /custom_countdown ros2_pkg/action/Ex5FullAction "{target_count: 5}"')

    def timer_callback(self):
        # ปั้นก้อน Message ส่งบอกสถานะ
        msg = Ex5FullMessage()
        msg.id = self.counter
        msg.name = "CustomRobo_Tx"
        msg.temperature = 35.0 + (self.counter % 5) * 0.5
        self.status_pub.publish(msg)
        self.counter += 1

    def service_callback(self, request, response):
        area = request.width * request.length
        response.area = area
        self.get_logger().info(f"[Service] ยืนยันรับคำขอ: กว้าง {request.width}, ยาว {request.length} -> คำนวณพื้นที่ได้ {area} ตร.ม.")
        
        # สั่งเต่าพุ่งเดิหน้าตามสเกลพื้นที่ที่ได้
        twist_msg = Twist()
        twist_msg.linear.x = float(area) / 2.0 # ย่อมันลงครึ่งนึงจะได้ไม่พุ่งชนกำแพงง่ายไป 
        self.cmd_vel_pub.publish(twist_msg)
        
        return response

    def action_execute_callback(self, goal_handle):
        self.get_logger().info(f"[Action] ตอบรับเป้าหมาย: เริ่มนับหมุนตัวช้าๆ {goal_handle.request.target_count} จังหวะ")
        
        feedback_msg = Ex5FullAction.Feedback()
        target = goal_handle.request.target_count
        
        for i in range(target):
            # หลับไปจังหวะละ 1 วิ
            time.sleep(1.0)
            
            # ส่งการอัปเดตสถานะกลับไปหาหน้าจอคนพิมพ์
            feedback_msg.current_count = i + 1
            goal_handle.publish_feedback(feedback_msg)
            self.get_logger().info(f"   => ส่งเต่าหมุนอยู่... ทำสำเร็จไปแล้ว {feedback_msg.current_count} ครั้ง")
            
            # สั่งเต่าหมุน
            twist_msg = Twist()
            twist_msg.angular.z = 2.0 # สร้างความเร็วเชิงมุม
            self.cmd_vel_pub.publish(twist_msg)
            
        # สำเร็จทั้งหมด
        goal_handle.succeed()
        result = Ex5FullAction.Result()
        result.completion_message = f"เรียบร้อย! หมุนไปครบสเต็ปที่ {target} แล้วครับเต่าหัวเกือบหมุน"
        self.get_logger().info("[Action] สำเร็จตามเป้าหมาย!")
        return result

def main(args=None):
    rclpy.init(args=args)
    node = CustomAllInOneNode()
    
    # ใช้จัดการด้ายการรันแยก (MultiThread) เพื่อรับประกันว่า Timer ไม่ถูกเบียดบังจังหวะ
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
        
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
