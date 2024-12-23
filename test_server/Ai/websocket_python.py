import asyncio
import websockets

# ฟังก์ชันสำหรับจัดการการเชื่อมต่อกับ client
async def handle_client(websocket):
    print("Client connected")
    try:
        while True:
            # รอรับข้อความจาก client
            message = await websocket.recv()
            print(f"Received: {message}")
            
            # ส่งข้อความกลับไปยัง client
            response = f"Server received: {message}"
            await websocket.send(response)
            print(f"Sent: {response}")

    except websockets.ConnectionClosed:
        print("Client disconnected")

# เริ่มต้น WebSocket Server
async def main():
    # สร้าง WebSocket server ที่รันบน localhost:9001
    server = await websockets.serve(handle_client, "localhost", 9001)
    print("WebSocket server started on ws://localhost:9001")

    # รอจนกว่าจะมีการปิดการเชื่อมต่อ
    await server.wait_closed()

# รัน Event Loop
asyncio.run(main())
