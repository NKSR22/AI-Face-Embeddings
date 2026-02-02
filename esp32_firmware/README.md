# ESP32 Smart Lock Firmware

This folder contains the source code for the ESP32 hardware used in the AI Face Recognition system.

## 📂 Contents
- `esp32_smart_lock.ino`: Main Arduino source code.
- `libraries/`: (Optional) Non-standard libraries required for this project.

## 🛠️ Installation
1. Open `esp32_smart_lock.ino` in **Arduino IDE**.
2. Go to **Tools > Board** and select **ESP32 Dev Module**.
3. Update the `ssid` and `password` variables with your WiFi credentials.
4. Click **Upload**.

## 🔌 Connection
- **IP Address**: After uploading, open the Serial Monitor (115200 baud) to find the ESP32's IP address.
- **Python App**: Enter this IP address in the GUI's IoT panel.
