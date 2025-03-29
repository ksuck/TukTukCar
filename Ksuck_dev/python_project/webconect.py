import json
from http.server import BaseHTTPRequestHandler, HTTPServer

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
        print("ข้อมูลที่ได้รับ:", data)

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

# ตั้งค่า HTTP server
def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

# เรียกใช้งาน server
if __name__ == "__main__":
    run()
