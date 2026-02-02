import cv2
import numpy as np
import os
import shutil
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir="known_faces", models_dir="models", tolerance=0.36):
        """
        ระบบจดจำใบหน้า (On-device Face Recognition System using OpenCV YuNet + SFace)
        :param known_faces_dir: Folder containing subfolders of verified users
        :param models_dir: Folder containing onnx models
        :param tolerance: Cosine similarity threshold (lower is more strict, default for SFace is around 0.36)
        """
        self.known_faces_dir = known_faces_dir
        self.tolerance = tolerance
        self.known_encodings = []
        self.known_names = []
        
        # Initialize models
        base_path = os.path.dirname(os.path.abspath(__file__))
        yunet_path = os.path.join(base_path, models_dir, "face_detection_yunet_2023mar.onnx")
        sface_path = os.path.join(base_path, models_dir, "face_recognition_sface_2021dec.onnx")
        
        if not os.path.exists(yunet_path) or not os.path.exists(sface_path):
            raise FileNotFoundError("Model files not found. Please run download_models.py first.")

        # YuNet Face Detector
        self.detector = cv2.FaceDetectorYN.create(
            model=yunet_path,
            config="",
            input_size=(320, 320),
            score_threshold=0.9,
            nms_threshold=0.3,
            top_k=5000
        )
        
        # SFace Face Recognizer
        self.recognizer = cv2.FaceRecognizerSF.create(
            model=sface_path,
            config=""
        )
        
        # Load known faces on initialization
        self.reload_faces()

    def reload_faces(self):
        """Reloads all known faces from the directory."""
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load images from known_faces directory and encode them."""
        print(f"[*] Loading known faces from '{self.known_faces_dir}'...")
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            return

        for entry in os.listdir(self.known_faces_dir):
            entry_path = os.path.join(self.known_faces_dir, entry)
            
            if os.path.isdir(entry_path):
                person_name = entry
                for image_name in os.listdir(entry_path):
                    if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                        self._process_image(os.path.join(entry_path, image_name), person_name)
            
            elif os.path.isfile(entry_path) and entry.lower().endswith((".jpg", ".jpeg", ".png")):
                person_name = os.path.splitext(entry)[0]
                self._process_image(entry_path, person_name)

        print(f"[*] Total known faces loaded: {len(self.known_names)} (from {len(set(self.known_names))} unique people)")

    def _process_image(self, image_path, name):
        """Helper to encode a single image file."""
        try:
            img = cv2.imread(image_path)
            if img is None: return
            
            # Update detector input size for high-res images
            self.detector.setInputSize((img.shape[1], img.shape[0]))
            _, faces = self.detector.detect(img)
            
            if faces is not None:
                # Use the first face detected
                face = faces[0]
                feature = self.recognizer.feature(self.recognizer.alignCrop(img, face))
                self.known_encodings.append(feature)
                self.known_names.append(name)
        except Exception as e:
            print(f"[!] Error loading {image_path}: {e}")

    def register_new_face(self, frame, name):
        """Save the frame as a new known face for the given name."""
        if not name:
            return False, "Name cannot be empty."

        person_dir = os.path.join(self.known_faces_dir, name)
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.jpg"
        image_path = os.path.join(person_dir, filename)
        
        # Detect and align before saving or just save the raw frame
        cv2.imwrite(image_path, frame)
        
        try:
            # Re-process to ensure we have features
            self.detector.setInputSize((frame.shape[1], frame.shape[0]))
            _, faces = self.detector.detect(frame)
            
            if faces is None:
                os.remove(image_path)
                return False, "No face detected in the captured image."

            feature = self.recognizer.feature(self.recognizer.alignCrop(frame, faces[0]))
            self.known_encodings.append(feature)
            self.known_names.append(name)
            return True, f"Success! {name} registered."
        except Exception as e:
            return False, f"Error encoding face: {e}"

    def recognize_faces(self, frame):
        """Process a frame and return locations and names."""
        # Update input size for current frame
        h, w, _ = frame.shape
        self.detector.setInputSize((w, h))
        
        _, faces = self.detector.detect(frame)
        
        face_locations = []
        face_names = []
        
        if faces is not None:
            for face in faces:
                # SFace matching
                feature = self.recognizer.feature(self.recognizer.alignCrop(frame, face))
                
                name = "Unknown"
                max_score = -1
                best_match_idx = -1
                
                for i, known_feature in enumerate(self.known_encodings):
                    # SFace match returns a similarity score (higher is more similar)
                    score = self.recognizer.match(feature, known_feature, cv2.FaceRecognizerSF_FR_COSINE)
                    
                    if score > self.tolerance and score > max_score:
                        max_score = score
                        best_match_idx = i
                
                if best_match_idx != -1:
                    name = self.known_names[best_match_idx]
                
                # Convert YuNet box to (top, right, bottom, left) for consistency with old code
                # YuNet box: [x, y, w, h, ...]
                x, y, w_box, h_box = map(int, face[:4])
                face_locations.append((y, x + w_box, y + h_box, x))
                face_names.append(name)
                
        return face_locations, face_names

    def get_registered_users(self):
        return sorted(list(set(self.known_names)))

    def delete_user(self, name):
        person_dir = os.path.join(self.known_faces_dir, name)
        if os.path.exists(person_dir):
            shutil.rmtree(person_dir)
            self.reload_faces()
            return True
        return False

def run_legacy_cli_mode():
    try:
        system = FaceRecognitionSystem()
    except Exception as e:
        print(f"[!] Initialization Error: {e}")
        return

    video_capture = cv2.VideoCapture(0)
    if not video_capture.isOpened():
        print("[!] Error: Could not open webcam.")
        return

    print("[*] Starting OpenCV Face Recognition...")
    print("    - Press 'q' to quit")
    print("    - Press 's' to save")

    while True:
        ret, frame = video_capture.read()
        if not ret: break

        face_locations, face_names = system.recognize_faces(frame)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.imshow('Face Recognition', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            name = input("Enter name: ")
            success, msg = system.register_new_face(frame, name)
            print(msg)

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_legacy_cli_mode()
