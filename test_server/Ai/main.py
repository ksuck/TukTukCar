import cv2
import numpy as np
from ultralytics import YOLO


# ตั้งค่าการเชื่อมต่อกับสตรีมจาก ESP32
url = 'http://building.local:82/stream'  # URL ของ ESP32 ที่ให้บริการสตรีม

# ใช้ OpenCV เพื่อเชื่อมต่อกับสตรีม
cap = cv2.VideoCapture(url)

# โหลดโมเดล YOLOv8
model = YOLO("C:/Users/build/Documents/test_server/Ai/yolo11n.pt")

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture image")
        break
    if ret:
        cv2.imshow("Defalt Esp32 Cam", frame)
        results = model(frame)  # ใช้ YOLOv8 ตรวจจับวัตถุ
        frame_ = results[0].plot()
        cv2.imshow("AI NAJA",frame_)

        if results[0].boxes.id is not None:
            #id
            track_ids = results[0].boxes.id.int().cpu()

            #box
            boxes = results[0].boxes.xyxy.cpu()
            
            

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
