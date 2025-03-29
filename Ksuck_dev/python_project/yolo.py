import cv2
import numpy as np
from ultralytics import YOLO
import os
import sys

# ตั้งค่าการเชื่อมต่อกับสตรีมจาก ESP32
url = 'http://building.local:82/stream'  # URL ของ ESP32 ที่ให้บริการสตรีม

color_array = [
    [0, 255, 0],    # สีเขียว
    [255, 0, 0],    # สีแดง
    [0, 0, 255],    # สีน้ำเงิน
    [255, 255, 0],  # สีเหลือง
    [0, 255, 255],  # สีฟ้า
    [255, 0, 255],  # สีม่วง
    [192, 192, 192], # สีเทา
    [0, 0, 0],      # สีดำ
    [255, 255, 255]  # สีขาว
]

meter_count = [0,0,0,0,0,0]


#find path now
script_folder = os.path.dirname(os.path.abspath(__file__))
print("Script Folder:", script_folder)


# ใช้ OpenCV เพื่อเชื่อมต่อกับสตรีม
cap = cv2.VideoCapture(0) #<-- 0 เพื่อใช้กล้องโน๊ตบุ๊ค เปลี่ยน 0 เป็น url เพื่อใช้ของ esp cam
image = cv2.imread(f'{script_folder}\\meter_test.jpg')
# โหลดโมเดล YOLOv8
model = YOLO(f'{script_folder}\\best_train.pt')

while True:
    ret, frame = cap.read()
    if not ret:
        if image is None:
            print("Failed to capture image")
            break
        else:
            # แสดงรูปภาพ
            cv2.imshow('My Image', image)
            image_copy = image.copy()
            results = model.track(image, persist=False, verbose=False)
            output_image = results[0].plot() 
            if results[0].boxes.id is not None:
                #id
                track_ids = results[0].boxes.id.int().cpu()

                #box
                boxes = results[0].boxes.xyxy.cpu()

                # Class IDs
                class_ids = results[0].boxes.cls.int().cpu().tolist()

                #Confidences
                confidences = results[0].boxes.conf.cpu().tolist()

                #name
                object_names = [model.names[int(cls_id)] for cls_id in class_ids]
                result_text = "\n".join(f'{obj}' for obj in object_names)

                #ดูรหัสแล้วตีกรอบตามรหัสกับสีที่ค่าความมั่นใจมากกว่า 5
                for i in range(len(class_ids)):
                     # เช็คว่าค่า Confidence >= 0.5 หรือไม่
                     if confidences[i] >= 0.5:
                        #print(f"Object {i+1}:")
                        #print(f"  Track ID: {track_ids[i]}")
                        #print(f"  Bounding Box: {boxes[i]}")
                        #print(f"  Class ID: {class_ids[i]}")
                        #print(f"  Class Name: {object_names[i]}")
                        #print(f"  Confidence: {confidences[i]:.2f}")  # พิมพ์ค่า Confidence
                        #print("-" * 30)


                        for x in range(10):
                            if class_ids[i] == x:
                                x1, y1, x2, y2 = map(int, boxes[i])  # แปลงค่าพิกัดเป็นจำนวนเต็ม

                                center_x = (x1 + x2) // 2
                                center_y = (y1 + y2) // 2

                                #print(boxes[i])
                                cv2.rectangle(image_copy, (x1, y1), (x2, y2), (color_array[x][0], color_array[x][1], color_array[x][2]), 2)
                                cv2.putText(image_copy,str(class_ids[i]),(center_x,center_y),cv2.FONT_HERSHEY_SIMPLEX,1,(color_array[x][0], color_array[x][1], color_array[x][2]),2)
                
                                break






            cv2.imshow('Best', output_image)
            cv2.imshow('CoppyFrame', image_copy)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
         
                 
    
    if ret:
        cv2.imshow("Defalt Esp32 Cam", frame)
        results = model.track(frame, persist=False, verbose=False)  # ใช้ YOLOv8 ตรวจจับวัตถุ
        frame_ = results[0].plot()
        cv2.imshow("AI NAJA",frame_)

        if results[0].boxes.id is not None:
            #id
            track_ids = results[0].boxes.id.int().cpu()

            #box
            boxes = results[0].boxes.xyxy.cpu()

             # Class IDs
            class_ids = results[0].boxes.cls.int().cpu().tolist()

            # Mapping Class IDs to Names
            object_names = [model.names[int(cls_id)] for cls_id in class_ids]

            result_text = "\n".join(f'{obj}' for obj in object_names)

            print(result_text)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
