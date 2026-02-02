# Privacy-Preserving Face Recognition System (On-Device)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Latest-green)](https://opencv.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-orange)](#)

[ภาษาไทยด้านล่าง]

# AI Face Embeddings & Recognition System (OpenCV YuNet + SFace)

[EN] A lightweight, high-performance face recognition system using **OpenCV YuNet** for face detection and **SFace** for generating facial embeddings. Designed for IoT integration and educational use.

[TH] ระบบจดจำใบหน้าประสิทธิภาพสูงและน้ำหนักเบา โดยใช้ **OpenCV YuNet** สำหรับการตรวจจับใบหน้า และ **SFace** สำหรับการสร้าง Facial Embeddings ออกแบบมาเพื่อการเชื่อมต่อ IoT และการใช้งานเพื่อการศึกษา

---

## 📋 Project Information | ข้อมูลโปรเจกต์

- **Course | รายวิชา:** ปัญญาประดิษฐ์เบื้องต้น
- **Department | สาขาวิชา:** สาขาวิศวกรรมไฟฟ้า
- **University | มหาวิทยาลัย:** มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตสกลนคร
- **Developer | ชื่อผู้พัฒนา:** อาจารย์นครินทร์ ศรีปัญญา

---

## 💡 About the Project | เกี่ยวกับโปรเจกต์

[EN] This project demonstrates a modern Face Recognition pipeline using **Native OpenCV DNN models**. It replaces the heavy dlib dependency with **YuNet** (ultra-fast face detection) and **SFace** (state-of-the-art recognition). This setup is fully compatible with **Python 3.13** on both Windows and Linux without complex build tools.

[TH] โปรเจกต์นี้สาธิตขั้นตอนการจดจำใบหน้าโดยใช้ **OpenCV DNN models** แบบ Native โดยเปลี่ยนจาก dlib ที่มีความซับซ้อนมาเป็น **YuNet** (ตรวจจับใบหน้ารวดเร็วพิเศษ) และ **SFace** (โมเดลจดจำใบหน้ายุคใหม่) ระบบรองรับ **Python 3.13** อย่างสมบูรณ์ทั้งบน Windows และ Linux โดยไม่ต้องติดตั้งเครื่องมือ Compile ที่ซับซ้อน

### Key Features | ฟีเจอร์เด่น

- **Native OpenCV:** No dlib/CMake required. Pure Python/OpenCV implementation.
- **Cross-Platform:** Seamless support for **Ubuntu** and **Windows**.
- **Real-time Performance:** YuNet detection optimized for high-speed tracking.
- **Modern Embeddings:** Uses Cosine Similarity for robust identity matching.

---

## 🚀 Quick Start | วิธีการเริ่มต้นใช้งาน

### 1. Environment Setup | การเตรียม Environment

```bash
# Create Virtual Environment | สร้าง venv
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 2. Installation | การติดตั้งไลบรารี

```bash
# Install Dependencies
pip install -r requirements.txt

# Download AI Models (Important!) | ดาวน์โหลดโมเดล AI
python download_models.py
```

---

## 🎮 Usage | วิธีการใช้งาน

### Graphical Interface (Recommended)
[TH] รันแอปพลิเคชัน GUI เพื่อเริ่มระบบตรวจจับและจดจำใบหน้า:
```bash
python gui.py
```

### Registration | การลงทะเบียนคนใหม่
1. พิมพ์ชื่อในช่อง **"New user name..."**
2. กดปุ่ม **CAPTURE FACE** เพื่อบันทึกใบหน้าและสร้าง Feature ทันที

---

## 🌐 GitHub Wiki & IoT (WiFi) Integration
[EN] This project can be expanded to connect with **IoT (WiFi)** devices like **ESP32** or **Arduino** to trigger actions (e.g., unlocking a door via MQTT or WebSockets).
[TH] โปรเจกต์นี้สามารถขยายฐานการทำงานเพื่อเชื่อมต่อกับอุปกรณ์ **IoT (WiFi)** เช่น **ESP32** เพื่อสั่งงานอุปกรณ์ภายนอก (เช่น ปลดล็อคประตูผ่าน MQTT หรือ WebSockets)

---

## 📖 Learning More | หัวข้อการเรียนรู้เพิ่มเติม

1. 🏛️ **[System Architecture](docs/ARCHITECTURE.md)**: การทำงานแบบ Multi-threading ใน PyQt6
2. 📐 **[Theory & Concept](docs/THEORY.md)**: ทฤษฎี YuNet, SFace และ Cosine Similarity
3. 🧪 **[Lab Manual](docs/LAB_MANUAL.md)**: ใบงานการทดลองและขั้นตอนปฏิบัติ
4. 🔌 **[Hardware & ESP32](docs/HARDWARE.md)**: วงจรฮาร์ดแวร์และโค้ดสำหรับ ESP32 Smart Lock

---

## 🛡️ Privacy & Local Processing
ระบบจดจำใบหน้านี้ทำงานแบบ **On-device 100%** ข้อมูลใบหน้าและ Feature ทั้งหมดถูกเก็บไว้ในเครื่อง ไม่มีการส่งข้อมูลไปยังระบบคลาวด์ภายนอก

---

## ⚖️ Copyright
Copyright © 2024 อาจารย์นครินทร์ ศรีปัญญา. All Rights Reserved.  
For educational purposes only at RMUTI Sakon Nakhon.
