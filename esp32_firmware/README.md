# ESP32 Smart Lock Firmware | เฟิร์มแวร์ ESP32 สำหรับกลอนประตูอัจฉริยะ

[EN] This folder contains the source code for the ESP32 hardware used in the AI Face Recognition system.
[TH] โฟลเดอร์นี้ประกอบด้วยซอร์สโค้ดสำหรับฮาร์ดแวร์ ESP32 ที่ใช้ในระบบจดจำใบหน้า AI

---

## 📂 Contents | สิ่งที่อยู่ภายใน
- `esp32_smart_lock.ino`: [EN] Main Arduino source code. [TH] ซอร์สโค้ดหลักสำหรับ Arduino
- `libraries/`: [EN] Non-standard libraries (if any). [TH] ไลบรารีเพิ่มเติม (ถ้ามี)

## 🛠️ Installation | การติดตั้ง
1. [EN] Open `esp32_smart_lock.ino` in **Arduino IDE**.
   [TH] เปิดไฟล์ `esp32_smart_lock.ino` ใน **Arduino IDE**
2. [EN] Go to **Tools > Board** and select **ESP32 Dev Module**.
   [TH] ไปที่เมนู **Tools > Board** และเลือก **ESP32 Dev Module**
3. [EN] Update the `ssid` and `password` variables with your WiFi credentials.
   [TH] แก้ไขตัวแปร `ssid` และ `password` ให้ตรงกับ WiFi ของคุณ
4. [EN] Click **Upload**.
   [TH] กดที่ปุ่ม **Upload**

## 🔌 Connection | การเชื่อมต่อ
- **IP Address**: [EN] After uploading, open the Serial Monitor (115200 baud) to find the ESP32's IP address.
  [TH] หลังจากอัปโหลดเสร็จ ให้เปิด Serial Monitor (115200 baud) เพื่อดู IP Address ของ ESP32
- **Python App**: [EN] Enter this IP address in the GUI's IoT panel.
  [TH] นำ IP Address นี้ไปใส่ในแผงควบคุม IoT ของโปรแกรม Python GUI
