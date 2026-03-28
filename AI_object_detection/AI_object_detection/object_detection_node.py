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

class ObjectDetectionNode(Node):
    def __init__(self):
        super().__init__('object_detection_node')
        
        # ให้ผู้ใช้งานระบุตำแหน่งไฟล์ Weights (.pt) ผ่าน Command line parameter ได้
        # Default เราจะใช้โมเดลจิ๋ว (yolov8n.pt) เพื่อจะได้ให้คอมช่วยโหลดอัตโนมัติมาเทสก่อน
        self.declare_parameter('weights', 'yolov8n.pt') 
        weights_path = self.get_parameter('weights').value
        
        self.bridge = CvBridge()
        
        if YOLO is None:
            self.get_logger().error("Cannot run object detection: ultralytics is missing.")
            self.model = None
        else:
            try:
                self.get_logger().info(f"Loading YOLO model from: {weights_path}")
                self.model = YOLO(weights_path)
            except Exception as e:
                self.get_logger().error(f"Failed to load YOLO model: {e}")
                self.model = None

        self.subscription = self.create_subscription(
            Image,
            '/robot1/camera/image_color',
            self.image_callback,
            10)
            
        self.get_logger().info("Object Detection Node started.")

    def image_callback(self, msg):
        if self.model is None:
            return
            
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            self.get_logger().error(f"Failed to convert image: {e}")
            return

        # Inference ด้วยโมเดลจาก ultralytics / Roboflow export
        results = self.model(cv_image, verbose=False)
        
        # นำกรอบ Bounding Box พร้อมค่าความแม่นยำมารวมกับภาพต้นฉบับ
        annotated_frame = results[0].plot()

        cv2.imshow("Roboflow YOLO Object Detection", annotated_frame)
        cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)
    node = ObjectDetectionNode()
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
