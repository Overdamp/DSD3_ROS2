# 🐢 สรุปขั้นตอนการสร้าง Robot Description Package (Ex6)

เป้าหมายของแพ็กเกจนี้คือการสร้างโมเดลตัวหุ่นยนต์ (URDF) และตั้งค่า **Robot State Publisher** รวมถึง **Joint State Publisher GUI** สำหรับโชว์โมเดลและปรับขยับล้อหุ่นโชว์ใน **RViz** ตามแนวทาง Best Practice ของ ROS 2

## โครงสร้างโฟลเดอร์ที่ถูกต้อง (Best Practice)
1. `urdf/` เซฟไฟล์กำหนดรูปร่างหุ่นยนต์ `.urdf` หรือ `.urdf.xacro`
2. `launch/` เซฟไฟล์ `.launch.py` สำหรับเรียกสคริปต์รันโหนด
3. `rviz/` เซฟฉากตั้งค่าหน้าตาจอ `.rviz` 
4. `meshes/` *(ถ้ามี)* เซฟไฟล์โมเดลสามมิติแบบเจาะจงเช่น `.stl`, `.dae`

---

## 🛠️ Step-by-Step การสร้างตั้งแต่ศูนย์
### Step 1: สร้าง Package พร้อม Dependencies สำคัญ
ใช้คำสั่งผ่าน Terminal:
```bash
ros2 pkg create --build-type ament_cmake ex6_turtlebot3_description \
  --dependencies urdf xacro robot_state_publisher joint_state_publisher_gui rviz2
```

### Step 2: สร้างและเขียนไฟล์ URDF
สร้างโฟลเดอร์ `urdf` และเขียนไฟล์ `turtlebot3_full.urdf` ออกแบบหุ่นยนต์แบบเป็นชิ้นๆ ประกอบกันด้วยระบบ `link` (ก้อนวัตถุ) และ `joint` (ข้อต่อ) เช่น ล้อซ้าย, ล้อขวา, ตัวถัง

### Step 3: สร้างและเขียนไฟล์ Launch
สร้างโฟลเดอร์ `launch` แล้วเขียนไฟล์ Python เพื่อควบคุมการรันโหนดหลัก 3 ตัวพร้อมกัน ได้แก่:
1. **robot_state_publisher:** โหนดที่คอยกระจายชิ้นส่วนพิกัดหุ่น (TF Tree) ตามที่กำหนดใน URDF สู่สากล
2. **joint_state_publisher_gui:** โหนดที่มีหน้าต่างแผงควบคุมสไลเดอร์เอาไว้ลากหมุนล้อเล่น (สั่งขยับแบบจำลอง Joint)
3. **rviz2:** ตัวโปรแกรมกราฟิกสำหรับใช้แสดงผลสิ่งที่เห็นทั้งหมด

### Step 4: ติดตั้ง Directories ใน CMakeLists.txt
เพื่อสร้างความมั่นใจว่าเวลาย้ายหุ่นไปรันในเครื่องอื่นหรือเวลาสั่ง `colcon build` ไดเรกทอรีที่สำคัญพวกนี้จะไม่ถูกลืม ให้เพิ่มโค้ดด้านล่างลงใน `CMakeLists.txt` ก่อนบรรทัด `ament_package()` เสมอ:
```cmake
install(DIRECTORY urdf launch rviz meshes
  DESTINATION share/${PROJECT_NAME}
)
```

### Step 5: ทดสอบ (Testing!)
Build โค้ดแล้วรันทดสอบโมเดลสวยๆ ผ่านคำสั่ง:
```bash
colcon build --symlink-install --packages-select ex6_turtlebot3_description
source install/setup.bash
ros2 launch ex6_turtlebot3_description rsp_gui_full.launch.py
```
*(ถ้าสไลด์แถบเลื่อนล้อแล้วในจอภาพล้อหมุนตาม แปลว่าสำเร็จ!)*
