import sys
import cv2
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QListWidget, 
                             QLineEdit, QFileDialog, QMessageBox, QFrame, 
                             QGridLayout, QScrollArea, QDialog)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QObject, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap, QFont, QAction

# Import backend
from main import FaceRecognitionSystem
import os
import time

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
        # Note: self.system.recognize_faces handles resizing internally for speed
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
            # Limit to ~30 FPS to save CPU
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
                count = 1 # legacy flat file
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
        self.setWindowTitle("CORTEX Face Detection")
        self.setGeometry(100, 100, 900, 700)
        
        # System Core
        self.system = FaceRecognitionSystem()
        
        # Database Window Instance
        self.db_window = None

        # Threading Setup
        self.setup_threads()
        
        # UI Setup
        self.setup_ui()

    def setup_threads(self):
        # 1. Video Capture Thread
        self.video_thread = VideoThread()
        self.video_thread.change_pixmap_signal.connect(self.update_feed_and_process)
        self.video_thread.start()

        # 2. Worker Thread for Recognition
        self.worker_thread = QThread()
        self.worker = RecognitionWorker(self.system)
        self.worker.moveToThread(self.worker_thread)
        
        # Connect signals
        self.frame_for_processing.connect(self.worker.process_frame)
        self.worker.result_signal.connect(self.handle_recognition_results)
        
        self.worker_thread.start()

        self.last_results = ([], []) # locations, names
        self.processing = False # Simple semaphore to drop frames if busy

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        central.setStyleSheet("background-color: #121212;")
        
        layout = QVBoxLayout(central)

        # Header
        top_bar = QHBoxLayout()
        title = QLabel("LIVE MONITORING")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #03dac6;")
        top_bar.addWidget(title)
        
        top_bar.addStretch()
        
        btn_db = QPushButton("Open Database")
        btn_db.setStyleSheet("background-color: #6200ee; color: white; padding: 8px 15px; font-weight: bold;")
        btn_db.clicked.connect(self.open_database)
        top_bar.addWidget(btn_db)
        
        layout.addLayout(top_bar)

        # Video Area
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 2px solid #333; background-color: #000;")
        self.image_label.setMinimumSize(640, 480)
        layout.addWidget(self.image_label, 1)

        # Bottom Controls (Quick Registration)
        controls = QFrame()
        controls.setStyleSheet("background-color: #1e1e1e; border-radius: 8px; padding: 10px;")
        c_layout = QHBoxLayout(controls)
        
        self.txt_name = QLineEdit()
        self.txt_name.setPlaceholderText("New user name...")
        self.txt_name.setStyleSheet("padding: 8px; background-color: #2d2d2d; color: white; border: 1px solid #444;")
        c_layout.addWidget(self.txt_name)
        
        btn_snap = QPushButton("CAPTURE FACE")
        btn_snap.setStyleSheet("background-color: #03dac6; color: black; font-weight: bold; padding: 8px 20px;")
        btn_snap.clicked.connect(self.quick_register)
        c_layout.addWidget(btn_snap)
        
        layout.addWidget(controls)
        
        # Status Bar
        self.status = QLabel("System Ready")
        self.status.setStyleSheet("color: #777; margin-top: 5px;")
        layout.addWidget(self.status)

    def update_feed_and_process(self, cv_img):
        """Called every time a new frame comes from the camera."""
        self.current_frame = cv_img.copy() # Store for capture
        
        # 1. Send for processing if worker is ready
        # To avoid lag, we don't block. We just fire the signal.
        # But if we send EVERY frame, the worker queue fills up and latentcy increases.
        # So we only send if we aren't "busy".
        if not self.processing:
            self.processing = True
            # Resize copy for processing? The worker calls recognize_faces which handles resizing.
            # Passing the full frame is fine if we suspect the worker is faster than 30fps (it's not).
            # So the worker might lag if we copy huge arrays.
            # But PyQt signals handle copying.
            self.frame_for_processing.emit(cv_img)

        # 2. Draw LAST KNOWN valid results on the CURRENT frame
        # This decouples the visual frame rate (30fps) from the recognition rate (e.g., 5-10fps)
        locations, names = self.last_results
        
        display_frame = cv_img.copy()
        for (top, right, bottom, left), name in zip(locations, names):
            # Scale coordinates back up
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255) # BGR
            cv2.rectangle(display_frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(display_frame, (left, bottom - 30), (right, bottom), color, cv2.FILLED)
            cv2.putText(display_frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        # Convert to Qt
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
        """Worker finished a frame."""
        self.last_results = (locations, names)
        self.processing = False
        
        # Optional: Print to status
        if names:
            self.status.setText(f"Detected: {', '.join(set(names))}")
        else:
            self.status.setText("Scanning...")

    def quick_register(self):
        name = self.txt_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Warn", "Enter a name first!")
            return
            
        if hasattr(self, 'current_frame'):
            # Pause processing briefly? No need.
            success, msg = self.system.register_new_face(self.current_frame, name)
            if success:
                QMessageBox.information(self, "Success", msg)
                self.txt_name.clear()
                # Reload needed? self.system internal list updates automatically in register_new_face
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
