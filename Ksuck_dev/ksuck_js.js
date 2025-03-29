document.addEventListener('contextmenu', event => event.preventDefault());

var slider1 = document.getElementById("Steering_wheel1");
var slider2 = document.getElementById("Steering_wheel2");
var count_slider = 0;

// ฟังก์ชันที่ใช้ในการอัปเดตค่า slider ทั้ง 2 ตัว
slider1.oninput = function() {
    // ปรับค่า slider2 ให้เหมือนกับ slider1
    slider2.value = this.value;
    count_slider = this.value 
    sendRangeValue();
};

slider2.oninput = function() {
    // ปรับค่า slider1 ให้เหมือนกับ slider2
    slider1.value = this.value;
    count_slider = this.value 
    sendRangeValue();
};

// การกดปุ่มให้เซตค่า slider
document.getElementById("servoLeft1").addEventListener("click", function() {
    slider1.value = "130";
    slider2.value = "130";
    count_slider = "130";  // อัปเดตค่า count_slider
    sendRangeValue();
});

document.getElementById("servoCenter1").addEventListener("mousedown", function() {
    slider1.value = "90";
    slider2.value = "90";
    count_slider = "90";  // อัปเดตค่า count_slider
    sendRangeValue();
});

document.getElementById("servoRight1").addEventListener("mousedown", function() {
    slider1.value = "50";
    slider2.value = "50";
    count_slider = "50";  // อัปเดตค่า count_slider
    sendRangeValue();
});

document.getElementById("servoLeft2").addEventListener("click", function() {
  slider1.value = "130";
  slider2.value = "130";
  count_slider = "130";  // อัปเดตค่า count_slider
  sendRangeValue();
});

document.getElementById("servoCenter2").addEventListener("mousedown", function() {
  slider1.value = "90";
  slider2.value = "90";
  count_slider = "90";  // อัปเดตค่า count_slider
  sendRangeValue();
});

document.getElementById("servoRight2").addEventListener("mousedown", function() {
  slider1.value = "50";
  slider2.value = "50";
  count_slider = "50";  // อัปเดตค่า count_slider
  sendRangeValue();
});

// ฟังก์ชันส่งค่าไปยัง ESP32
function sendRangeValue() {
    let value = count_slider;  // แปลงค่าให้เป็นตัวเลข (โดยใช้ parseInt) ถ้าจำเป็น
    console.log("Sending value:", value);  // ตรวจสอบค่าที่ส่งไป

    // ส่งค่าผ่าน HTTP GET request ไปยัง ESP32
    fetch(`http://ksuck.local:8080/setSteering?value=${value}`)
        .then(response => response.text())
        .then(data => console.log(data))  // พิมพ์ข้อมูลที่ได้รับจาก ESP32
        .catch(error => console.error('Error:', error));
}



function sendClick(buttonId) {
  const data = { message: "capture" };  // ข้อมูลที่จะส่ง

      fetch('http://localhost:8080', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then(response => response.json())
      .then(data => {
        console.log('ข้อมูลที่ได้รับจาก Python:', data);
      })
      .catch(error => {
        console.error('เกิดข้อผิดพลาด:', error);
      });
}

function controlLED(state) {
  fetch(`http:/ksuck.local:8080/led`)
  .then(response => response.text())
  .then(data => console.log("Response from ESP32:", data))
  .catch(error => console.error("Error:", error));
}

// เลือกปุ่มด้วย id
var moveAutoButton = document.getElementById("moveAuto");
var isAutoActive = true;
// เพิ่ม event listener ให้กับปุ่ม
moveAutoButton.addEventListener("click", function() {
  // ตรวจสอบสถานะของปุ่มและสลับสี
  if (this.style.backgroundColor === "red") {
    // ถ้าปัจจุบันสีเป็นแดง เปลี่ยนกลับเป็นสีเดิม
    this.style.backgroundColor = "";
    this.style.color = "";  // เปลี่ยนสีตัวอักษรกลับเป็นปกติ
    isAutoActive = true;
  } else {
    // ถ้าปัจจุบันสีไม่เป็นแดง เปลี่ยนเป็นสีแดง
    this.style.backgroundColor = "red";
    this.style.color = "white";  // เปลี่ยนสีตัวอักษรเป็นสีขาว
    isAutoActive = false;
  }
});

var moveForward = document.getElementById("moveForward");
var moveBackward = document.getElementById("moveBackward");
var moveLeft = document.getElementById("moveLeft");
var moveRight = document.getElementById("moveRight");
var moveStop = document.getElementById("moveStop");

// กำหนด event listener สำหรับปุ่มควบคุมทิศทาง
moveForward.addEventListener("mousedown", function() {
  sendControlCommand('forward');
});

moveForward.addEventListener("mouseup", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

moveForward.addEventListener("touchstart", function() {
  sendControlCommand('forward');
});

moveForward.addEventListener("touchend", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

// ปุ่มสำหรับ Move Backward
moveBackward.addEventListener("mousedown", function() {
  sendControlCommand('backward');
});

moveBackward.addEventListener("mouseup", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

moveBackward.addEventListener("touchstart", function() {
  sendControlCommand('backward');
});

moveBackward.addEventListener("touchend", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

// ปุ่มสำหรับ Move Left
moveLeft.addEventListener("mousedown", function() {
  sendControlCommand('left');
});

moveLeft.addEventListener("mouseup", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

moveLeft.addEventListener("touchstart", function() {
  sendControlCommand('left');
});

moveLeft.addEventListener("touchend", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

// ปุ่มสำหรับ Move Right
moveRight.addEventListener("mousedown", function() {
  sendControlCommand('right');
});

moveRight.addEventListener("mouseup", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

moveRight.addEventListener("touchstart", function() {
  sendControlCommand('right');
});

moveRight.addEventListener("touchend", function() {
if (isAutoActive) {
  sendControlCommand('stop');
}
});

// ปุ่มหยุดการทำงาน
moveStop.addEventListener("mousedown", function() {
    sendControlCommand('stop');
});
moveStop.addEventListener("touchstart", function() {
    sendControlCommand('stop');
});

// ฟังก์ชันส่งคำขอไปยัง ESP32
function sendControlCommand(action) {
    console.log(`Sending action: ${action}`);
    fetch(`http://ksuck.local:8080/${action}`)
        .then(response => response.text())
        .then(data => console.log("Response from ESP32:", data))
        .catch(error => console.error("Error:", error));
}


//กัน esp32 หลุด
/*
var nothing = "led";  // ค่าเริ่มต้น

// ฟังก์ชันส่งค่าทุก 1 วินาที
setInterval(function() {
    console.log("Sending keep-alive:",led );
    fetch(`http://ksuck.local:8080/${led}`)
        .then(response => response.text())
        .then(data => console.log("Response from ESP32:", data))
        .catch(error => console.error("Error:", error));
}, 1000); // ส่งทุก 1 วินาที*/