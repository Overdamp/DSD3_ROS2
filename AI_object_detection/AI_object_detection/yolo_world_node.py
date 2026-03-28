#!/usr/bin/env python3
import os
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

try:
    from ultralytics import YOLO
except ImportError:
    YOLO = None
    print("Warning: 'ultralytics' library not installed. Please run 'pip install ultralytics'")

class YoloWorldNode(Node):
    def __init__(self):
        super().__init__('yolo_world_node')
        
        # รับค่าคำศัพท์เป้าหมาย (Prompt) ผ่าน Arguments ยกตัวอย่างค่าเบื้องต้นคือกล่องกระดาษและกำแพง
        self.declare_parameter('target_classes', 'cardboard box,door,window,tree')
        target_classes_str = self.get_parameter('target_classes').value
        
        # คัดแยกข้อความที่มีคอมม่า (,) ย่นให้กลายเป็น List ในไพธอน
        self.target_classes = [c.strip() for c in target_classes_str.split(',') if c.strip()]
        
        self.bridge = CvBridge()
        
        if YOLO is None:
            self.get_logger().error("Cannot run YOLO-World: ultralytics is missing.")
            self.model = None
        else:
            try:
                self.get_logger().info("กำลังโหลดโมเดลอัจฉริยะ YOLOv8s-World (Zero-Shot)...")
                # โหลดโมเดล YOLO-World อัตโนมัติ (จะโหลดจากเน็ตถ้าไม่มีอยู่)
                self.model = YOLO('yolov8s-world.pt')
                
                # *** ทีเด็ด: กำหนดให้มันหาอะไรก็ได้ตามที่เราพิมพ์เข้ามา ***
                self.model.set_classes(self.target_classes)
                self.get_logger().info(f"👉 กำลังสแกนหาวัตถุเหล่านี้: {self.target_classes}")
                
            except Exception as e:
                self.get_logger().error(f"Failed to load YOLO-World model: {e}")
                self.model = None

        self.subscription = self.create_subscription(
            Image,
            '/robot1/camera/image_color',
            self.image_callback,
            10)
            
        self.get_logger().info("YOLO-World Node พร้อมทำงานแล้ว รอรับภาพจากซิมมูเลเตอร์...")

    def image_callback(self, msg):
        if self.model is None:
            return
            
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # สั่งคำนวณและกวาดหาของแบบ Zero-Shot 
        results = self.model(cv_image, verbose=False)
        
        # เอาผลลัพธ์มาวาดทับรูประหว่างทางโชว์
        annotated_frame = results[0].plot()

        cv2.imshow("YOLO-World Zero-Shot AI", annotated_frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = YoloWorldNode()
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
