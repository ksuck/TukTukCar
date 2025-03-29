#include <WiFi.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <ESP32Servo.h>

const char *ssid = "Ksuck";
const char *password = "5555555555";
WebServer server(8080);

Servo myservo;

int led_logic = 0;

void led_func() {
    server.sendHeader("Access-Control-Allow-Origin", "*");
    server.send(200);
}

void steering() {
  if (server.hasArg("value")) {
    String value = server.arg("value");
    Serial.println("Steering value received: " + value);
    // สามารถใช้ค่าที่ได้รับมาควบคุมมอเตอร์หรืออุปกรณ์อื่นๆได้ 90 50
    int steeringValue = value.toInt();
    myservo.write(steeringValue);
    // เพิ่มโค้ดที่นี่เพื่อควบคุมฮาร์ดแวร์ตามค่าที่ได้รับ
  }
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", "Value received");
}

void motor_forward() {
  Serial.println("forward");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", "Value received");
  digitalWrite(26,LOW);
  digitalWrite(27,HIGH);
  digitalWrite(32,LOW);
  digitalWrite(33,HIGH);

}

void motor_backward() {
  Serial.println("backward");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", "Value received");
  digitalWrite(26,HIGH);
  digitalWrite(27,LOW);
  digitalWrite(32,HIGH);
  digitalWrite(33,LOW);
}

void motor_moveleft() {
  Serial.println("moveleft");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", "Value received");

  digitalWrite(26,HIGH);
  digitalWrite(27,LOW);
  digitalWrite(32,LOW);
  digitalWrite(33,HIGH);
}

void motor_moveright() {
  Serial.println("moveright");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", "Value received");
  
  digitalWrite(26,LOW);
  digitalWrite(27,HIGH);
  digitalWrite(32,HIGH);
  digitalWrite(33,LOW);
}

void motor_stop() {
  Serial.println("stop");
  server.sendHeader("Access-Control-Allow-Origin", "*");
  server.send(200, "text/plain", "Value received");

  digitalWrite(26,LOW);
  digitalWrite(27,LOW);
  digitalWrite(32,LOW);
  digitalWrite(33,LOW);
}

void setup() {
  Serial.begin(115200);
  //
  myservo.attach(25); 
  myservo.write(90);
  pinMode(26, OUTPUT);
  pinMode(27, OUTPUT);
  pinMode(32, OUTPUT);
  pinMode(33, OUTPUT);

  //สแกน wifi
  Serial.println("Scanning for networks...");
  int numNetworks = WiFi.scanNetworks();  // สแกนหา Wi-Fi

  Serial.print("Found ");
  Serial.print(numNetworks);
  Serial.println(" networks");

  // แสดงรายชื่อ SSID และความแรงของสัญญาณ (RSSI)
  for (int i = 0; i < numNetworks; i++) {
    Serial.print("Network: ");
    Serial.println(WiFi.SSID(i));  // ชื่อเครือข่าย (SSID)
    Serial.print("Signal Strength (RSSI): ");
    Serial.println(WiFi.RSSI(i));  // ความแรงของสัญญาณ
    Serial.println("--------------------");
  }

  Serial.println("Connecting to WiFi...");
  // เชื่อมต่อกับ Wi-Fi
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  // รอจนกว่าจะเชื่อมต่อสำเร็จ
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }

  // เมื่อเชื่อมต่อสำเร็จ
  Serial.println("");
  Serial.println("WiFi connected");
  //Serial.print("IP Address: ");
  //Serial.println(WiFi.localIP());  // แสดง IP address ของ ESP32
  //Serial.print("Camera Stream Ready! Visit: http://");
  Serial.println(WiFi.localIP());
  if (!MDNS.begin("ksuck")) {  // เปลี่ยน "myesp" เป็นชื่อที่คุณต้องการ
    Serial.println("Error starting mDNS");
    return;
  }

  MDNS.addService("http", "tcp", 8080);
  Serial.println("You can access your ESP32 at http:/ksuck.local/");

  // Define routes
  server.on("/led", led_func);
  server.on("/setSteering", steering);
  //motor
  server.on("/forward", motor_forward);
  server.on("/backward", motor_backward);
  server.on("/left", motor_moveleft);
  server.on("/right", motor_moveright);
  server.on("/stop", motor_stop);

  // Start the server
  server.begin();
}

void loop() {
  server.handleClient();
}