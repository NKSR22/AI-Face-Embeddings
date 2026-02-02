import sys
import cv2
import numpy as np
import requests
import threading
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QListWidget, 
                             QLineEdit, QFileDialog, QMessageBox, QFrame, 
                             QGridLayout, QScrollArea, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject, pyqtSlot, QTimer
from PyQt6.QtGui import QImage, QPixmap, QFont, QAction

# Import backend
from main import FaceRecognitionSystem
import os
import time
from datetime import datetime

# --- Worker for Face Recognition (Fixes CPU Lag) ---
class RecognitionWorker(QObject):
    result_signal = pyqtSignal(object, object, object) # frame, locations, names

    def __init__(self, system):
        super().__init__()
        self.system = system
        self.running = True

    @pyqtSlot(np.ndarray)
    def process_frame(self, frame):
        if not self.running: return
        
        # Run recognition
        locations, names = self.system.recognize_faces(frame)
        self.result_signal.emit(frame, locations, names)

# --- Thread for Video Capture ---
class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                self.change_pixmap_signal.emit(frame)
            time.sleep(0.033) 
        cap.release()

    def stop(self):
        self._run_flag = False
        self.wait()

# --- Separate Window based on User Request ---
class DatabaseWindow(QMainWindow):
    def __init__(self, system):
        super().__init__()
        self.system = system
        self.setWindowTitle("Face Database Manager")
        self.setGeometry(200, 200, 600, 500)
        self.setStyleSheet("""
            QMainWindow { background-color: #252526; color: white; }
            QWidget { font-family: 'Segoe UI', sans-serif; }
            QListWidget { background-color: #1e1e1e; border: 1px solid #333; color: #ddd; }
            QPushButton { background-color: #3d3d3d; color: white; border-radius: 4px; padding: 6px; }
            QPushButton:hover { background-color: #505050; }
            QLabel { color: #ccc; }
        """)
        
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)

        # List
        self.user_list = QListWidget()
        self.user_list.itemClicked.connect(self.load_details)
        layout.addWidget(self.user_list, 1)

        # Details
        details = QFrame()
        d_layout = QVBoxLayout(details)
        
        self.lbl_name = QLabel("Select User")
        self.lbl_name.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self.lbl_name.setStyleSheet("color: #4CAF50;")
        d_layout.addWidget(self.lbl_name)

        self.lbl_info = QLabel("Images: -")
        d_layout.addWidget(self.lbl_info)

        btn_add = QPushButton("Upload Photo")
        btn_add.clicked.connect(self.upload_photo)
        d_layout.addWidget(btn_add)

        btn_del = QPushButton("Delete User")
        btn_del.setStyleSheet("background-color: #d32f2f;")
        btn_del.clicked.connect(self.delete_user)
        d_layout.addWidget(btn_del)
        
        d_layout.addStretch()
        
        btn_refresh = QPushButton("Refresh List")
        btn_refresh.clicked.connect(self.refresh_list)
        d_layout.addWidget(btn_refresh)

        layout.addWidget(details, 1)
        
        self.refresh_list()

    def refresh_list(self):
        self.user_list.clear()
        users = self.system.get_registered_users()
        self.user_list.addItems(users)

    def load_details(self, item):
        name = item.text()
        self.lbl_name.setText(name)
        user_dir = os.path.join(self.system.known_faces_dir, name)
        
        count = 0
        if os.path.exists(user_dir):
            if os.path.isdir(user_dir):
                count = len([f for f in os.listdir(user_dir) if f.lower().endswith(('.jpg','.png'))])
            else:
                count = 1 
        self.lbl_info.setText(f"Images: {count}")

    def upload_photo(self):
        name = self.lbl_name.text()
        if name == "Select User": return
        
        path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.jpg *.png)")
        if path:
            img = cv2.imread(path)
            if img is not None:
                success, msg = self.system.register_new_face(img, name)
                QMessageBox.information(self, "Result", msg)
                self.load_details(self.user_list.currentItem())
            else:
                QMessageBox.warning(self, "Error", "Could not read image.")

    def delete_user(self):
        name = self.lbl_name.text()
        if name == "Select User": return
        
        if QMessageBox.question(self, "Confirm", f"Delete {name}?") == QMessageBox.StandardButton.Yes:
            self.system.delete_user(name)
            self.refresh_list()
            self.lbl_name.setText("Select User")
            self.lbl_info.setText("Images: -")


# --- Main Detection Window ---
class DetectionWindow(QMainWindow):
    # Signals to worker
    frame_for_processing = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CORTEX Face Detection & IoT Control")
        self.setGeometry(100, 100, 1100, 750)
        
        # System Core
        self.system = FaceRecognitionSystem()
        self.db_window = None

        # IoT Control Variables
        self.esp32_ip = "192.168.1.100" # Default IP
        self.iot_cooldown = 10 # Seconds
        self.last_iot_trigger = 0
        self.iot_enabled = False

        self.setup_threads()
        self.setup_ui()

    def setup_threads(self):
        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_feed_and_process)
        self.video_thread.start()

        self.worker_thread = QThread()
        self.worker = RecognitionWorker(self.system)
        self.worker.moveToThread(self.worker_thread)
        self.frame_for_processing.connect(self.worker.process_frame)
        self.worker.result_signal.connect(self.handle_recognition_results)
        self.worker_thread.start()

        self.last_results = ([], []) 
        self.processing = False 

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #121212;")
        
        main_layout = QHBoxLayout(central)

        # Left Column (Video)
        left_col = QVBoxLayout()
        
        top_bar = QHBoxLayout()
        title = QLabel("LIVE MONITORING")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #03dac6;")
        top_bar.addWidget(title)
        top_bar.addStretch()
        
        btn_db = QPushButton("Open Database")
        btn_db.setStyleSheet("background-color: #3d3d3d; color: white; padding: 5px 15px;")
        btn_db.clicked.connect(self.open_database)
        top_bar.addWidget(btn_db)
        left_col.addLayout(top_bar)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #333; background-color: #000;")
        self.image_label.setMinimumSize(640, 480)
        left_col.addWidget(self.image_label, 1)

        # Registration Panel
        reg_panel = QFrame()
        reg_panel.setStyleSheet("background-color: #1e1e1e; border-radius: 8px; padding: 10px;")
        reg_layout = QHBoxLayout(reg_panel)
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("New user name...")
        self.txt_name.setStyleSheet("padding: 8px; background-color: #2d2d2d; color: white; border: 1px solid #444;")
        reg_layout.addWidget(self.txt_name)
        btn_snap = QPushButton("CAPTURE FACE")
        btn_snap.setStyleSheet("background-color: #03dac6; color: black; font-weight: bold; padding: 8px 15px;")
        btn_snap.clicked.connect(self.quick_register)
        reg_layout.addWidget(btn_snap)
        left_col.addWidget(reg_panel)

        self.status = QLabel("System Ready")
        self.status.setStyleSheet("color: #777; margin-top: 5px;")
        left_col.addWidget(self.status)

        main_layout.addLayout(left_col, 3)

        # Right Column (IoT & Settings)
        right_col = QVBoxLayout()
        iot_panel = QFrame()
        iot_panel.setStyleSheet("background-color: #1e1e1e; border-radius: 8px; padding: 15px;")
        iot_layout = QVBoxLayout(iot_panel)

        iot_title = QLabel("IoT / WiFi CONTROL")
        iot_title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        iot_title.setStyleSheet("color: #bb86fc;")
        iot_layout.addWidget(iot_title)

        iot_layout.addWidget(QLabel("ESP32 / Device IP:"))
        self.txt_ip = QLineEdit(self.esp32_ip)
        self.txt_ip.setStyleSheet("padding: 8px; background-color: #2d2d2d; color: white;")
        iot_layout.addWidget(self.txt_ip)

        self.btn_iot_toggle = QPushButton("ENABLE IoT TRIGGER")
        self.btn_iot_toggle.setCheckable(True)
        self.btn_iot_toggle.setStyleSheet("background-color: #3d3d3d; color: white; padding: 10px; font-weight: bold;")
        self.btn_iot_toggle.clicked.connect(self.toggle_iot)
        iot_layout.addWidget(self.btn_iot_toggle)

        iot_layout.addSpacing(10)
        btn_test = QPushButton("TEST UNLOCK")
        btn_test.clicked.connect(self.trigger_iot_action)
        iot_layout.addWidget(btn_test)

        self.iot_log = QListWidget()
        self.iot_log.setStyleSheet("background-color: #121212; color: #888; font-size: 10px;")
        iot_layout.addWidget(QLabel("Action Logs:"))
        iot_layout.addWidget(self.iot_log)

        right_col.addWidget(iot_panel)
        right_col.addStretch()
        main_layout.addLayout(right_col, 1)

    def toggle_iot(self):
        self.iot_enabled = self.btn_iot_toggle.isChecked()
        self.esp32_ip = self.txt_ip.text().strip()
        if self.iot_enabled:
            self.btn_iot_toggle.setStyleSheet("background-color: #bb86fc; color: black; padding: 10px; font-weight: bold;")
            self.log_iot("IoT Trigger Enabled")
        else:
            self.btn_iot_toggle.setStyleSheet("background-color: #3d3d3d; color: white; padding: 10px; font-weight: bold;")
            self.log_iot("IoT Trigger Disabled")

    def log_iot(self, msg):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.iot_log.insertItem(0, f"[{timestamp}] {msg}")

    def trigger_iot_action(self):
        """Sends a request to the ESP32 in a separate thread to avoid UI freezing."""
        ip = self.txt_ip.text().strip()
        url = f"http://{ip}/unlock" # Assumes ESP32 has an /unlock endpoint
        
        def send_request():
            try:
                self.log_iot(f"Sending trigger to {ip}...")
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    self.log_iot("Success: Unlock command sent.")
                else:
                    self.log_iot(f"Failed: HTTP {response.status_code}")
            except Exception as e:
                self.log_iot(f"Error: {str(e)}")

        threading.Thread(target=send_request, daemon=True).start()

    def update_feed_and_process(self, cv_img):
        self.current_frame = cv_img.copy()
        if not self.processing:
            self.processing = True
            self.frame_for_processing.emit(cv_img)

        locations, names = self.last_results
        display_frame = cv_img.copy()
        for (top, right, bottom, left), name in zip(locations, names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(display_frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            cv2.putText(display_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        rgb_image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        qt_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.image_label.setPixmap(QPixmap.fromImage(qt_img).scaled(
            self.image_label.width(), self.image_label.height(), 
            Qt.AspectRatioMode.KeepAspectRatio
        ))

    @pyqtSlot(object, object, object)
    def handle_recognition_results(self, frame, locations, names):
        self.last_results = (locations, names)
        self.processing = False
        
        if names:
            detected_known = [n for n in names if n != "Unknown"]
            if detected_known:
                self.status.setText(f"Welcome, {', '.join(set(detected_known))}!")
                
                # Check for IoT Trigger
                if self.iot_enabled:
                    current_time = time.time()
                    if current_time - self.last_iot_trigger > self.iot_cooldown:
                        self.last_iot_trigger = current_time
                        self.log_iot(f"Match found: {detected_known[0]}")
                        self.trigger_iot_action()
            else:
                self.status.setText("Scanning (Unknown face detected)")
        else:
            self.status.setText("Scanning...")

    def quick_register(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Warn", "Enter a name first!")
            return
            
        if hasattr(self, 'current_frame'):
            success, msg = self.system.register_new_face(self.current_frame, name)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.txt_name.clear()
            else:
                QMessageBox.warning(self, "Error", msg)

    def open_database(self):
        if self.db_window is None:
            self.db_window = DatabaseWindow(self.system)
        self.db_window.refresh_list()
        self.db_window.show()
        self.db_window.raise_()

    def closeEvent(self, event):
        self.video_thread.stop()
        self.worker.running = False
        self.worker_thread.quit()
        self.worker_thread.wait()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DetectionWindow()
    window.show()
    sys.exit(app.exec())
