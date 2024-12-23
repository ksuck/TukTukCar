import paho.mqtt.client as mqtt

# กำหนดที่อยู่ของ MQTT broker
broker_address = "localhost"  # หรือ IP ของเครื่องที่รัน Mosquitto
port = 1883
topic = "car_control"

# ตั้งค่า MQTT Client
client = mqtt.Client()

# ฟังก์ชันเมื่อเชื่อมต่อกับ MQTT broker
def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    # ส่งคำสั่งควบคุมรถ (ตัวอย่าง)
    client.subscribe("car_control")

    '''
    
    client.publish(topic, "FORWARD")  # ส่งคำสั่งให้ไปข้างหน้า
    client.publish(topic, "BACKWARD")  # ส่งคำสั่งให้ถอยหลัง
    client.publish(topic, "STOP")      # ส่งคำสั่งให้หยุด
    '''
# Callback เมื่อได้รับข้อความจาก MQTT broker
def on_message(client, userdata, msg):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")
    # ที่นี่สามารถใส่การดำเนินการเพิ่มเติมหลังจากรับข้อมูล เช่นการส่งคำสั่งไปที่อุปกรณ์


# กำหนด callback function
client.on_connect = on_connect
client.on_message = on_message

# เชื่อมต่อกับ MQTT broker
client.connect(broker_address, port, 60)

# เริ่มต้นการรับและส่งข้อความ
client.loop_forever()


# ให้โปรแกรมรันไปเรื่อยๆ เพื่อรอรับข้อมูล
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Program interrupted.")
    client.loop_stop()  # หยุดการฟังเมื่อโปรแกรมถูกยกเลิก


'''
เปิด mqtt port 1883
net start mosquitto

ปิด 
net stop mosquitto

คำสั่งส่งค่า            สั่งเป็น pub         ip           topic           text
user terminal test mosquitto_pub -h localhost -t car_control -m "Hello world"

'''