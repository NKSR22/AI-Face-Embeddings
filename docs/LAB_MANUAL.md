# Lab Manual | ใบงานการทดลอง

## 🎯 Objective | วัตถุประสงค์
[EN] To understand the workflow of a modern face recognition system and its integration with IoT devices.
[TH] เพื่อทำความเข้าใจขั้นตอนการทำงานของระบบจดจำใบหน้าสมัยใหม่และการเชื่อมต่อกับอุปกรณ์ IoT

## 📋 Prerequisites | สิ่งที่ต้องเตรียม
- [EN] Computer with Python & Webcam. [TH] คอมพิวเตอร์พร้อมกล้อง Webcam
- [EN] ESP32 (Optional). [TH] บอร์ด ESP32 (ถ้ามี)

## 🧪 Step-by-Step | ขั้นตอนปฏิบัติ
### 1. Model Deployment | การติดตั้งโมเดล
1. Install dependencies using `pip install -r requirements.txt`.
2. Execute `python download_models.py` and observe the ONNX model files in the `models/` folder.
3. **Question**: Why do we use ONNX instead of raw Python code for models?

### 2. Face Registration | การลงทะเบียนใบหน้า
1. Run `python gui.py`.
2. Register your face using the **CAPTURE FACE** button.
3. Observe how a new folder is created inside `known_faces/`.

### 3. Face Identification | การระบุตัวตน
1. Show your face to the camera.
2. Observe the green/red bounding boxes and the identification results.
3. Test with different lighting conditions and angles.

### 4. IoT Integration | การทำงานร่วมกับ IoT
1. Enter the IP address of your ESP32 in the IoT panel.
2. Toggle the **ENABLE IoT TRIGGER**.
3. Observe the Logs when a match is found.
4. **Task**: Explain how the "Cooldown" mechanism helps save resources and prevents hardware stress.

### 5. Hardware Implementation | การติดตั้งฮาร์ดแวร์
1. Refer to [HARDWARE.md](HARDWARE.md) for the wiring diagram.
2. Flash the provided Arduino code to your ESP32.
3. Connect the Relay and Solenoid Lock according to the schematic.
4. **Test**: Use the **TEST UNLOCK** button in the Python app and verify the Solenoid Lock physically clicks open.

## 📝 Discussion | ประเด็นการสนทนา
- [EN] How does the system handle "Unknown" people? [TH] ระบบจัดการกับคนแปลกหน้าที่ไม่รู้จักอย่างไร?
- [EN] Privacy implications? [TH] ผลกระทบด้านความเป็นส่วนตัวมีอะไรบ้าง?
