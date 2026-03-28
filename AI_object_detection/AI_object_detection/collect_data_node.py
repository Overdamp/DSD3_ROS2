#!/usr/bin/env python3
import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
from datetime import datetime

class DataCollectorNode(Node):
    def __init__(self):
        super().__init__('collect_data_node')
        self.declare_parameter('save_dir', 'collect_data')
        self.save_dir = self.get_parameter('save_dir').value
        
        # สร้างโฟลเดอร์สำหรับเก็บภาพถ้ายังไม่มี
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)
            self.get_logger().info(f"Created direct directory: {os.path.abspath(self.save_dir)}")

        # Subscribe ตัวกล้องที่เราเสริมให้หุ่น
        self.subscription = self.create_subscription(
            Image,
            '/robot1/camera/image_color',
            self.image_callback,
            10)
        self.bridge = CvBridge()
        self.get_logger().info("Data Collector Node started. Select OpenCV window and press 's' (or 'S') to save image.")

    def image_callback(self, msg):
        try:
            # แปลงภาพจาก ROS Message (sensor_msgs/Image) เป็นภาพสีแบบ BGR ของ OpenCV
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        cv2.imshow("Camera View (Press 's' to Save Image)", cv_image)
        key = cv2.waitKey(1) & 0xFF

        # ถ้ากดเปิดคีย์บอร์ดแล้วกดตัว s จะบันทึกภาพ
        if key == ord('s') or key == ord('S'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = os.path.join(self.save_dir, f"img_{timestamp}.jpg")
            cv2.imwrite(filename, cv_image)
            self.get_logger().info(f"✅ Saved image to >> {filename}")


def main(args=None):
    rclpy.init(args=args)
    node = DataCollectorNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
