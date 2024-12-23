#include <WiFi.h>
#include <PubSubClient.h>

// กำหนดข้อมูล WiFi
const char *ssid = "Hor Pak May Sa 2";
const char *password = "5555555555";

// กำหนดข้อมูล MQTT
const char *mqtt_server = "localhost"; // หรือ IP ของเครื่องที่รัน MQTT Broker
const int mqtt_port = 1883;
const char *mqtt_topic = "car_control";

// กำหนดขา GPIO สำหรับมอเตอร์
const int motorPin1 = 12;  // ขา GPIO สำหรับมอเตอร์ 1
const int motorPin2 = 13;  // ขา GPIO สำหรับมอเตอร์ 2

WiFiClient espClient;
PubSubClient client(espClient);

// ฟังก์ชันสำหรับเชื่อมต่อ WiFi
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
}

// ฟังก์ชันสำหรับเชื่อมต่อ MQTT
void reconnect() {
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
      client.subscribe(mqtt_topic); // Subscribe ไปที่ topic "car_control"
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

// ฟังก์ชันสำหรับรับคำสั่งจาก MQTT
void callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Message arrived: ");
  Serial.println(message);

  if (message == "FORWARD") {
    // ส่งคำสั่งให้มอเตอร์ไปข้างหน้า
    digitalWrite(motorPin1, HIGH);
    digitalWrite(motorPin2, LOW);
  }
  else if (message == "BACKWARD") {
    // ส่งคำสั่งให้มอเตอร์ถอยหลัง
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, HIGH);
  }
  else if (message == "STOP") {
    // ส่งคำสั่งให้มอเตอร์หยุด
    digitalWrite(motorPin1, LOW);
    digitalWrite(motorPin2, LOW);
  }
}

void setup() {
  // เริ่มต้น Serial
  Serial.begin(115200);

  // เชื่อมต่อ WiFi
  setup_wifi();

  // กำหนดขา GPIO สำหรับมอเตอร์
  pinMode(motorPin1, OUTPUT);
  pinMode(motorPin2, OUTPUT);

  // เชื่อมต่อ MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
