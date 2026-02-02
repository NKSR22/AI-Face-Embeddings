# Theory & Concept | ทฤษฎีและแนวคิด

[EN] This page explains the core AI models used in this system.
[TH] หน้านี้อธิบายเกี่ยวกับโมเดล AI หลักที่ใช้ในระบบนี้

---

## 1. Face Detection: YuNet | การตรวจจับใบหน้า: YuNet
[EN] YuNet is a lightweight and efficient face detection model based on Convolutional Neural Networks (CNN). 
- **Efficiency**: Optimized for CPU/Edge devices.
- **Accuracy**: Robust against various scales, viewpoints, and occlusions.
- **Output**: 15 key points including bounding box coordinates and facial landmarks.

[TH] YuNet เป็นโมเดลตรวจจับใบหน้าที่มีน้ำหนักเบาและมีประสิทธิภาพสูง พัฒนาบนฐานของ Convolutional Neural Networks (CNN)
- **ประสิทธิภาพ**: ปรับแต่งมาเพื่อใช้งานบน CPU และอุปกรณ์พกพา
- **ความแม่นยำ**: ทนทานต่อการเปลี่ยนแปลงขนาด มุมมอง และการถูกบดบัง
- **ผลลัพธ์**: ให้จุดสำคัญ 15 จุด รวมถึงพิกัดกรอบใบหน้าและจุดเด่นบนใบหน้า (ตา จมูก ปาก)

## 2. Face Recognition: SFace | การจดจำใบหน้า: SFace
[EN] SFace is a deep learning-based face recognition model that generates facial embeddings.
- **Embeddings**: A face is compressed into a high-dimensional feature vector.
- **Metric Learning**: The model ensures images of the same person are mathematically close.

[TH] SFace เป็นโมเดลจดจำใบหน้าที่ใช้ Deep Learning เพื่อสร้างค่า Facial Embeddings
- **Embeddings**: ใบหน้าจะถูกบีบอัดให้กลายเป็นเวกเตอร์คุณลักษณะที่มีหลายมิติ
- **Metric Learning**: โมเดลถูกเทรนมาเพื่อให้ภาพของคนคนเดียวกันมีค่าทางคณิตศาสตร์ที่ใกล้เคียงกัน

## 3. Comparison: Cosine Similarity | การเปรียบเทียบ: Cosine Similarity
[EN] This system uses **Cosine Similarity** to match faces.
- **Range**: -1 to 1 (Higher is more similar).
- **Threshold**: In this project, we use **0.36**. If the score is higher, it's a match.

[TH] ระบบนี้ใช้ **Cosine Similarity** ในการเปรียบเทียบใบหน้า
- **ช่วงค่า**: -1 ถึง 1 (ค่ายิ่งสูงยิ่งมีความคล้ายคลึงมาก)
- **เกณฑ์การตัดสิน (Threshold)**: ในโปรเจกต์นี้เราใช้ค่า **0.36** หากคะแนนสูงกว่านี้จะถือว่าเป็นบุคคลคนเดียวกัน

## 4. Privacy & Data | ความเป็นส่วนตัวและข้อมูล
[EN] All computations happen **locally**. No biometric data is sent to the cloud.
[TH] การประมวลผลทั้งหมดเกิดขึ้น**ภายในเครื่อง** ไม่มีการส่งข้อมูลดิบหรือข้อมูลอัตลักษณ์ไปยังระบบคลาวด์
