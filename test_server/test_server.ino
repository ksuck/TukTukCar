#include <WiFi.h>
#include <ESPmDNS.h>
//config camera
#include "esp_camera.h"
#include "camera_config.h"

//select wifi
const char *ssid = "Hor Pak May Sa 2";
const char *password = "5555555555";

void startCameraServer();
void setupLedFlash(int pin);

void setup() {
  Serial.begin(115200);
  Serial.setDebugOutput(true);
  Serial.println();

  // เรียกใช้การตั้งค่ากล้องจาก camera_config.h
  camera_config_t config = getCameraConfig();

  // เริ่มต้นกล้อง
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Camera init failed!");
    return;
  }
  //-----------------------------------------

  //สแกน wifi
  Serial.println("Scanning for networks...");
  int numNetworks = WiFi.scanNetworks(); // สแกนหา Wi-Fi

  Serial.print("Found ");
  Serial.print(numNetworks);
  Serial.println(" networks");

  // แสดงรายชื่อ SSID และความแรงของสัญญาณ (RSSI)
  for (int i = 0; i < numNetworks; i++) {
    Serial.print("Network: ");
    Serial.println(WiFi.SSID(i)); // ชื่อเครือข่าย (SSID)
    Serial.print("Signal Strength (RSSI): ");
    Serial.println(WiFi.RSSI(i)); // ความแรงของสัญญาณ
    Serial.println("--------------------");
  }

  Serial.println("Connecting to WiFi...");
  // เชื่อมต่อกับ Wi-Fi
  WiFi.begin(ssid, password);

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
  //Serial.println(WiFi.localIP());
  if (!MDNS.begin("building")) { // เปลี่ยน "myesp" เป็นชื่อที่คุณต้องการ
    Serial.println("Error starting mDNS");
    return;
  }

  //เริ่มใช้งานกล้อง
  startCameraServer();
  Serial.println("You can access your ESP32 at http:/building.local/");
}

void loop() {
  // put your main code here, to run repeatedly:
}
