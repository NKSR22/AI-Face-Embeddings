# Privacy-Preserving Face Recognition System (On-Device)

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Latest-green)](https://opencv.org/)

[ภาษาไทยด้านล่าง]

# AI Face Embeddings & Recognition System

[EN] An educational platform for learning modern face recognition techniques using Local Binary Patterns (LBP), Histograms of Oriented Gradients (HOG), and Deep Metric Learning (Embeddings).

[TH] แพลตฟอร์มเพื่อการศึกษาสำหรับการเรียนรู้เทคนิคการจดจำใบหน้าสมัยใหม่ โดยใช้ LBP, HOG และ Deep Metric Learning (Embeddings)

---

## 📋 Project Information | ข้อมูลโปรเจกต์

- **Course | รายวิชา:** ปัญญาประดิษฐ์เบื้องต้น
- **Department | สาขาวิชา:** สาขาวิศวกรรมไฟฟ้า
- **University | มหาวิทยาลัย:** มหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตสกลนคร
- **Developer | ชื่อผู้พัฒนา:** อาจารย์นครินทร์ ศรีปัญญา

---

## 💡 About the Project | เกี่ยวกับโปรเจกต์

[EN] This project demonstrates an end-to-end Face Recognition pipeline. It utilizes **dlib** for high-precision face landmark detection and **face_recognition** (OpenFace/ResNet-based) to generate 128D facial embeddings. The system supports multi-face detection, real-time tracking, and a graphical database management system.

[TH] โปรเจกต์นี้สาธิตขั้นตอนการจดจำใบหน้าแบบครบวงจร (End-to-end) โดยใช้ **dlib** สำหรับการตรวจจับจุดเด่นบนใบหน้า (Landmarks) ที่มีความแม่นยำสูง และใช้ **face_recognition** (ฐานการทำงานจาก OpenFace/ResNet) เพื่อสร้าง Facial Embeddings ขนาด 128 มิติ ระบบรองรับการตรวจจับได้หลายใบหน้าพร้อมกัน การติดตามแบบ Real-time และระบบจัดการฐานข้อมูลผ่านหน้าจอ GUI

### Key Features | ฟีเจอร์เด่น

- **Real-time Recognition:** Decoupled processing for smooth 30+ FPS visual feedback.
- **Embedded Database:** Store multiple reference images per individual for increased accuracy.
- **Multi-face Support:** Detect and identify multiple people in a single frame simultaneously.
- **GUI Management:** Easy-to-use interface built with PyQt6 for user registration and database cleanup.

---

## 🚀 Quick Start | วิธีการเริ่มต้นใช้งาน

### 1. Environment Setup | การเตรียม Environment

[EN] It is recommended to use a Virtual Environment (venv) to manage dependencies.
[TH] แนะนำให้ใช้ Virtual Environment (venv) ในการจัดการไลบรารีต่างๆ

```powershell
# Create Virtual Environment | สร้าง venv
python -m venv venv

# Activate (Windows) | การเรียกใช้งาน
.\venv\Scripts\activate
```

### 2. Installation | การติดตั้งไลบรารี

```powershell
# Upgrade pip | อัปเกรดตัวติดตั้ง
python -m pip install --upgrade pip

# Install Dependencies | ติดตั้งไลบรารีที่จำเป็น
pip install -r requirements.txt
```

---

## 🎮 Usage | วิธีการใช้งาน

[EN] The project provides two modes of operation. For production and teaching, the GUI mode is recommended.
[TH] โปรเจกต์มีโหมดการทำงาน 2 รูปแบบ แนะนำให้ใช้งาน GUI mode สำหรับการเรียนการสอน

### Graphical Interface (Recommended)

[EN] Run the GUI application using VS Code or terminal:
[TH] รันแอปพลิเคชัน GUI ผ่าน VS Code หรือ Terminal:

```powershell
python gui.py
```

### CLI Support (Legacy/Testing)

[EN] For lightweight testing without a GUI:
[TH] สำหรับการทดสอบเบื้องต้นแบบไม่มี GUI:

```powershell
python main.py
```

---

## 📖 Learning More | หัวข้อการเรียนรู้เพิ่มเติม

[EN] Access detailed technical documentation through our GitHub Wiki:
[TH] อ่านเอกสารทางเทคนิคและคู่มือการทดลองได้ผ่าน GitHub Wiki:

1. 🏛️ **[System Architecture](https://github.com/YourRepo/wiki/System-Architecture)**: Understand the data flow and threading model.
2. 📐 **[Theory & Concept](https://github.com/YourRepo/wiki/Theory-Concept)**: Dive into HOG and Face Embeddings logic.
3. 🧪 **[Lab Manual](https://github.com/YourRepo/wiki/Lab-Manual)**: Step-by-step experiment for students.

---

## ⚖️ Copyright

Copyright © 2024 [Your Name]. All Rights Reserved.  
For educational purposes only.

If you encounter issues on Windows (especially Python 3.13):

- **Missing dlib:** The `requirements.txt` already includes a direct link to a pre-built dlib wheel for Python 3.13. If you use a different Python version, you might need to find a matching wheel.
- **Model not found:** Ensure `setuptools` is installed (`pip install setuptools`) to help Python 3.13 discover the model files.

### Usage

1. Prepare known faces:
   - **Option A (Manual):** Add `.jpg` or `.png` images to the `known_faces/` folder and rename them to the person's name.
   - **Option B (Auto):** Run the program and press **'s'** to capture the face currently in view. You will be prompted for a name in the console.
2. Run the system:

   ```bash
   python main.py
   ```

3. Controls:
   - **'q'**: Quit the application.
   - **'s'**: Save/Register current face.

---

## ระบบจดจำใบหน้าแบบเน้นความเป็นส่วนตัว (Local Processing)

ระบบจดจำใบหน้าแบบ Real-time ที่ประมวลผลบนเครื่อง 100% โดยอ้างอิงสถาปัตยกรรม FaceNet (Schroff et al., 2015) เพื่อความรวดเร็วและปลอดภัยของข้อมูลส่วนบุคคล

## ✨ คุณสมบัติ

- **ประมวลผล Local 100%:** ข้อมูลใบหน้าไม่ถูกส่งไปยัง Server ภายนอก เน้นความเป็นส่วนตัว
- **โหลดข้อมูลอัตโนมัติ:** ระบบจะโหลดภาพจากโฟลเดอร์ `known_faces/`
- **[ใหม่] โหมดถ่ายภาพ (Capture Mode):** สามารถเพิ่มสมาชิกใหม่ได้ทันทีโดยการกดปุ่ม **'s'** และตั้งชื่อผ่าน Console
- **Optimize ประสิทธิภาพ:** มีการย่อขนาดภาพ (Resizing) และประมวลผลแบบเว้นเฟรม (Frame Skipping) เพื่อให้ใช้งานได้ลื่นไหล
- **การตรวจจับที่แม่นยำ:** ใช้การคำนวณ Euclidean Distance ในการเปรียบเทียบใบหน้า พร้อมปรับค่า Tolerance ได้

## 🚀 เริ่มต้นใช้งาน

### สิ่งที่ต้องเตรียม

- Python 3.10 ขึ้นไป (รองรับ 3.13)
- เว็บแคม (Webcam)

### การติดตั้ง

1. (แนะนำ) สร้างและเปิดใช้งาน Virtual Environment:

   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

2. ติดตั้งเครื่องมือและ Library ที่จำเป็น:

   ```bash
   # จำเป็นสำหรับ Python 3.13
   pip install setuptools wheel
   
   # ติดตั้ง Library ทั้งหมด (รวมถึง dlib สำหรับ 3.13)
   pip install -r requirements.txt
   ```

### 🛠️ การแก้ปัญหา (สำหรับ Windows)

หากคุณพบข้อผิดพลาดบน Windows:

- **ติดตั้ง dlib ไม่ได้:** ใน `requirements.txt` ได้ใส่ลิงก์ตรงสำหรับ dlib บน Python 3.13 ไว้ให้แล้ว หากคุณใช้ Python เวอร์ชันอื่น อาจต้องหาไฟล์ `.whl` ที่ตรงกันมาติดตั้ง
- **หา Model ไม่เจอ:** ตรวจสอบให้แน่ใจว่าได้ติดตั้ง `setuptools` แล้ว เพื่อให้ Python 3.13 มองเห็นไฟล์ Model
- **ขาด C++ Compiler:** หากต้องคอมไพล์ Library เอง ให้ติดตั้ง **Visual Studio Build Tools** (Desktop development with C++) [ที่นี่](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### วิธีใช้งาน

1. **การเพิ่มสมาชิก:**
   - **วิธีที่ 1:** นำรูปภาพใบหน้า (`.jpg`, `.png`) ไปใส่ในโฟลเดอร์ `known_faces/` และตั้งชื่อไฟล์ตามชื่อคน
   - **วิธีที่ 2:** เมื่อรันโปรแกรมแล้ว ให้กดปุ่ม **'s'** เพื่อถ่ายภาพหน้าปัจจุบัน แล้วพิมพ์ชื่อในหน้าจอ Console
2. **เริ่มรันระบบ:**

   ```bash
   python main.py
   ```

3. **ปุ่มควบคุม:**
   - **'q'**: เพื่อออกจากโปรแกรม
   - **'s'**: เพื่อถ่ายภาพหน้าและบันทึกชื่อสมาชิกใหม่

## 📄 License

Project developed for educational purposes.
