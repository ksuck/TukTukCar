import cv2
import numpy as np
from ultralytics import YOLO

# ตั้งค่าการเชื่อมต่อกับสตรีมจาก ESP32
url = 'http://building.local//stream'  # URL ของ ESP32 ที่ให้บริการสตรีม

# ใช้ OpenCV เพื่อเชื่อมต่อกับสตรีม
cap = cv2.VideoCapture(url)

# โหลดโมเดล YOLOv8
model = YOLO("C:\\Users\\build\\Documents\\test_server\Ai\\yolo11n.pt")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break
    
    # ตรวจจับวัตถุด้วย YOLOv8
    results = model.track(frame , persist=False, verbose=False)#จำกัดจำนวน [0]

    # แสดงผลการตรวจจับ
    results.show()  # แสดงภาพที่ตรวจจับ

    # ถ้าต้องการเก็บภาพที่ตรวจจับได้:
    # results.save()  # บันทึกภาพ

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
