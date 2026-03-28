# สรุปโค้ด ROS 2 (อิงจาก turtlesim)

โค้ดทั้งหมดที่ให้มาแบ่งเป็น 3 ส่วนหลักตามรูปแบบการสื่อสารใน ROS 2 (Robot Operating System) ได้แก่ **โหนดแบบ Publisher/Subscriber**, **แบบ Service-Client**, และ **แบบ Action-Client** โดยแต่ละโฟลเดอร์มีทั้งไฟล์เต็ม (`full_*.py`) สำหรับเป็นตัวอย่างเฉลย และไฟล์โครง (`skeleton_*.py`) สำหรับเว้นช่องว่างไว้ฝึกเขียน

## 1. Topic (Publisher / Subscriber)
ใช้สำหรับส่งข้อมูลต่อเนื่องแบบแพร่กระจายทางเดียว (Broadcast)
- **Publisher (`ex1_pub_sub/full_pub.py`)**
  - **หน้าที่:** ส่งคำสั่งความเร็ว (Velocity) ให้เต่าขยับ
  - **Topic:** `/turtle1/cmd_vel`
  - **ชนิดข้อความ (Message Type):** `geometry_msgs.msg/Twist`
  - **การทำงาน:** สร้าง `Timer` ให้ทำงานทุกๆ 0.5 วินาที แล้วส่งค่าความเร็วเชิงเส้น (เดินหน้า `linear.x = 2.0`) และความเร็วเชิงมุม (เลี้ยว `angular.z = 1.8`) ออกไป ทำให้เต่าวาดรูปเป็นวงกลมบนหน้าจอ
- **Subscriber (`ex1_pub_sub/full_sub.py`)**
  - **หน้าที่:** รับข้อมูลตำแหน่งปัจจุบันของเต่าแล้วแสดงผล
  - **Topic:** `/turtle1/pose`
  - **ชนิดข้อความ (Message Type):** `turtlesim.msg/Pose`
  - **การทำงาน:** รับค่าตำแหน่งพิกัด x, y ตลอดเวลาแบบ Real-time และเรียกใช้คอลแบ็กฟังก์ชัน (`pose_callback`) เพื่อปริ้นท์พิกัดนั้นออกทางหน้าจอเรื่อยๆ

## 2. Service
ใช้สำหรับส่งคำขอและป้อนกลับคำตอบ (Request/Response) ซึ่งจะมีฝั่งเรียกใช้งาน (Client) และฝั่งให้บริการ (Server)
- **Service Client (`ex2_service/full_srv.py`)**
  - **หน้าที่:** สั่งวาร์ป (Teleport) เต่าไปตำแหน่งที่ระบุทันที 
  - **Service Name:** `/turtle1/teleport_absolute`
  - **ชนิดข้อความ (Service Type):** `turtlesim.srv/TeleportAbsolute`
  - **การทำงาน:** สร้าง Client แล้วเตรียมข้อมูลคำขอ (Request) ระบุพิกัดเป้าหมายแบบเจาะจง `(x=2.0, y=2.0, theta=0.0)` การส่งข้อมูลเป็นแบบดึงข้อมูลกลับแบบไม่รอจังหวะบล็อกโค้ด (Asynchronous `call_async`) แต่เนื่องจากสั่งวาร์ปครั้งเดียวจบ จึงใช้ `rclpy.spin_once(node)` เพื่อรอรับผลแค่ครั้งเดียวแล้วจบโปรแกรม

## 3. Action
ใช้สำหรับงานที่ใช้เวลาทำงานระดับหนึ่งหรือใช้เวลานาน (Long-running process) โดยสามารถส่งกลับสถานะความคืบหน้า (Feedback) ได้และสามารถสั่งยกเลิกกลางคันได้
- **Action Client (`ex3_action/full_action.py`)**
  - **หน้าที่:** สั่งให้เต่าหันทำมุม/หมุนตัวตามเป้าหมาย และรับค่าความคืบหน้าระหว่างที่เต่ากำลังค่อยๆ หัน
  - **Action Name:** `/turtle1/rotate_absolute`
  - **ชนิดข้อความ (Action Type):** `turtlesim.action/RotateAbsolute`
  - **การทำงาน:** เตรียมเป้าหมาย (Goal) เป็นการหมุนให้ได้มุม `theta = 3.14` (ชี้ไปทางซ้ายมือคือทำระดับ 180 องศา) ไปให้ Action Server เมื่อผู้ส่งกำลังส่งเป้าหมาย (`send_goal_async`) จะส่งฟังก์ชันคอยรับสถานะ (`feedback_callback`) แนบไปด้วย ในโค้ดตัวอย่าง `feedback_callback` จะปริ้นท์ค่า `remaining` (ระยะมุมที่เหลือต้องหมุนอีกเท่าไหร่ถึงจะถึงเป้า) เรื่อยๆ จนกว่าเต่าจะหันจบเสร็จสมบูรณ์

## 4. Launch Files
ใช้สำหรับรันหลายๆ Node พร้อมกันด้วยคำสั่งเดียวเพื่อความสะดวกในการจัดการลดการพิมพ์คำสั่งหลายหน้าต่าง
- **Launch File (`launch/ex4_launch/full.launch.py`)**
  - **หน้าที่:** รัน Node ของ **turtlesim** (`turtlesim_node`) และ Node **Publisher** (`full_pub.py`) ที่เราเขียนขึ้นมาพร้อมกัน
  - **การทำงาน:** โค้ดจะใช้ `LaunchDescription` เพื่อรวมลิสต์ของ `Node` ต่างๆ ที่ต้องการรัน โดยกำหนด `package`, `executable`, และ `name` ของ Node เป้าหมาย เมื่อรันไฟล์นี้ (`ros2 launch ros2_pkg full.launch.py`) ระบบจะรันซิมูเลเตอร์เต่าและโปรแกรมควบคุมเต่าขึ้นมาเองทั้งหมด

## 5. Custom Message / Service / Action (Ex5)
การสร้างโครงสร้างข้อมูลชุดใหม่ขึ้นมาใช้เอง สำหรับงานเฉพาะเจาะจงที่ ROS 2 ไม่มีให้:
- **Topic Message (`msg/Ex5FullMessage.msg`)**: กำหนดตัวแปรสำหรับรับส่งแบบทิศทางเดียว (เช่น `id`, `name`, `temperature`)
- **Service (`srv/Ex5FullService.srv`)**: แบ่งเป็นโซน Request ส่งไป และ Response ตอบกลับ (คั่นด้วย `---`) (เช่น ส่ง `width`, `length` แล้วตอบ `area`)
- **Action (`action/Ex5FullAction.action`)**: แบ่งเป็นโซน Goal, Result, และ Feedback (คั่นด้วย `---`) (เช่น ส่ง `target_count` ไป แล้วรับ `current_count` กลับมาระหว่างทาง)
- **ตัวอย่างโค้ดเรียกใช้งาน (`scripts/ex5_custom_msg/ex5_full_custom.py`)**: เป็น Node แบบออลอินวันอเนกประสงค์ (All-in-One) เพื่อใช้เชื่อมโยง Custom Message ของเราเข้ากับเครื่องมือสั่งตัวซิมูเลเตอร์เต่า (`turtlesim_node`) ในกระบวนการเดียว:
  1. ใช้ **Publisher** บรอดแคสต์ `Ex5FullMessage` ปลอมรายงานสถานะตัวเองออกทาง Topic `/robot_info` 
  2. เปิดเครื่องเซิร์ฟเวอร์รอลูกค้า **Service** (`/custom_move`) ซึ่งรอรับตัวแปรความกว้าง/ยาวของชนิด `Ex5FullService` มาคำนวณหาพื้นที่ และสั่งนำแรงที่ได้ไปดันเต่าเดินหน้าทันที
  3. เปิดเครื่องเซิร์ฟเวอร์ตอบรับ **Action** (`/custom_countdown`) คอยรับตัวเลขของชนิด `Ex5FullAction` มานับถอยหลังพร้อมกับใช้แรงกระทำสั่งให้เต่าหมุนตัวช้าๆ เป็นจังหวะ
  *(พร้อมระบุคำสั่งเรียกทดสอบ CLI สำหรับยิงข้อมูลไปให้โหนดตัวนี้เอาไว้ให้ดูในโค้ดแล้วครับ)*

*(นอกจากนี้ยังมีไฟล์ `Ex5Skeleton*` ทั้งสามรูปแบบ สำหรับฝึกลองประกาศตัวแปรตามที่มีเครื่องหมาย TODO ไว้ให้)*

> [!NOTE] 
> การประกาศ Custom Message จะต้องไปตั้งค่าเพิ่มใน `CMakeLists.txt` (ใช้ `rosidl_generate_interfaces(...)`) และ `package.xml` เสมอ เพื่อให้คอมไพเลอร์ของ ROS สร้างโค้ด Python/C++ ให้สามารถทำ import ได้

## ไฟล์โครงสร้าง (Skeleton Files)
ทุกตัวอย่างจะมีไฟล์ `skeleton_*.py` และ `.launch.py` ซึ่งเว้นว่างส่วนโค้ดหลักที่เป็นหัวใจสำคัญโดยทำเครื่องหมาย `# TODO` ไว้เพื่อให้ฝึกเขียน:
- **`skeleton_pub.py` / `skeleton_sub.py`**: เว้นการสร้าง Publisher, กำหนดค่าความเร็วและ Publish และเว้นการสร้าง Subscriber เพื่อรับ Pose
- **`skeleton_srv.py`**: เว้นการสร้าง Service Client, สร้าง Request Parameter และการส่งคำร้องขอ
- **`skeleton_action.py`**: เว้นการสร้าง Action Client, การสร้างและกำหนด Goal Message รวมถึงการผูก Feedback Callback ตอนปริ้นท์ความคืบหน้า
- **`skeleton.launch.py`**: เว้นโครงสร้างการตั้งค่าพารามิเตอร์ภายใน `Node()` เพื่อให้ฝึกเขียนเชื่อมโยง Package และ Executable ร่วมกันใน LaunchDescription
