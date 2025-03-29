#open cv
from ultralytics import YOLO
import cv2
import numpy as np
import requests
#
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
#os
import os



class RequestHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        # ส่งการตอบกลับสำหรับคำขอ OPTIONS
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_POST(self):
        # รับข้อมูลจาก request
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # แปลงข้อมูล JSON
        data = json.loads(post_data)

        # แสดงข้อมูลที่ได้รับ
        #print("ข้อมูลที่ได้รับ:", data)
        ksuck.process(data)

        # ส่งข้อมูลตอบกลับ
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')  # เพิ่มการรองรับ CORS
        self.end_headers()
        response = {
            "status": "success",
            "received_data": data
        }
        self.wfile.write(json.dumps(response).encode('utf-8'))


class object_code:
    #global 

    #defalt 
    def __init__(self, server_class, port, token_key, url_post, dir_ai, url_espcam):
        #http
        self.server_class =  server_class
        self.port = port

        #data respone 
        self.data_respone = None
        
        #line
        self.token_key = token_key
        self.url_post = url_post

        self.header = {
            'Authorization': 'Bearer ' + self.token_key
        }
        
        #ai
        self.dir_ai = dir_ai 
        self.model = YOLO(dir_ai)

        
        #esp32
        self.url_espcam = url_espcam

    def process(self, data):
        # รับข้อมูลที่ส่งมาจาก RequestHandler
        #print("ข้อมูลที่ได้รับใน ObjectCode:", data)

        # สมมติว่าทำการประมวลผลบางอย่าง
        self.data_respone = data['message']
        return  self.data_respone

    #camera setting
    def cam_setting(self,setting_cam = 0):
        if setting_cam == 0:
            self.cap = cv2.VideoCapture(0)
        elif setting_cam == 1:
            self.cap = cv2.VideoCapture(self.url_espcam)
            
    #main run หลัก
    def run(self):
        threading.Thread(target=self.web_respone).start()
        threading.Thread(target=self.real_time_detection).start()

    def real_time_detection(self):
        

        #response = requests.post(self.url_post, headers=self.header, data=data
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to capture image")
                break

            if ret:
                #cv2.imshow("Defalt Cam", frame) #<---- ปิด comment เพื่อ show กล้อง
                results = self.model.track(frame, persist=False, verbose=False)  # ใช้ YOLOv8 ตรวจจับวัตถุ
                frame_ = results[0].plot()
                #cv2.imshow("AI NAJA",frame_)

                

                if  self.data_respone != None:
                    filename = 'image.png' #<---- ชื่อรูปที่จะเซฟ
                    cv2.imwrite(filename, frame_)  # บันทึกรูปภาพเป็นไฟล์ PNG

                    if results[0].boxes.id is not None:
                        

                         # Class IDs
                        class_ids = results[0].boxes.cls.int().cpu().tolist()

                        # Mapping Class IDs to Names
                        self.object_names = [self.model.names[int(cls_id)] for cls_id in class_ids]
                        self.result_text = "\n".join(f'{obj}' for obj in self.object_names)

                    else:
                        self.object_names = None
                        self.result_text = None
                    

                    try:
                        img = {'imageFile': open(filename,'rb')} #Local picture File
                        data = {'message': f'-- รูป --'}
                        data2 = {'message': f'\n หาวัตถุเจอทั้งหมด {len(self.object_names)}\n{self.result_text}'}

                    #session = requests.Session()
                        session = requests.Session()
                        session_post = session.post(self.url_post, headers=self.header, files=img , data=data)
                        session_post = session.post(self.url_post, headers=self.header, data=data2)
                    
                        if session_post.status_code == 200:
                            self.data_respone = None 
                    except:
                        pass
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break        
    

    def web_respone(self):
        server_address = ('', port)
        httpd = server_class(server_address, RequestHandler)
        print(f'Starting server on port {port}...')
        httpd.serve_forever()
      


if __name__ == "__main__":
    #line 
    token_key = "il0qsfUabxa9EpkE3u9OBo28wGofV1adhF256BWBQAf" #<--- notify api key
    url_post = "https://notify-api.line.me/api/notify" #<--- defalt line notify api
    
    #yolo
    dir_model = "C:\\xampp\\htdocs\\Ksuck_dev\\python_project\\best_train.pt" #<--- direct yolov

    #esp32
    url_esp32 = 'http://building.local:82/stream' # <--- url stream

    #web setting 
    server_class=HTTPServer
    port=8080

    ksuck = object_code(server_class,port,token_key,url_post,dir_model,url_esp32)
    ksuck.cam_setting(1) #<--- ตั้งค่ากล้อง 0 เป็นกล้องบนโน๊ตบุ๊ค 1 กล้องจาก esp32 cam
    ksuck.run()