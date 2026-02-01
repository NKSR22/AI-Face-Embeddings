import cv2
import face_recognition
import numpy as np
import os
import time
import shutil
from datetime import datetime

class FaceRecognitionSystem:
    def __init__(self, known_faces_dir="known_faces", tolerance=0.6):
        """
        ระบบจดจำใบหน้า (On-device Face Recognition System)
        :param known_faces_dir: Folder containing subfolders of verified users
        :param tolerance: Lower is more strict, default is 0.6
        """
        self.known_faces_dir = known_faces_dir
        self.tolerance = tolerance
        self.known_encodings = []
        self.known_names = []
        
        # Load known faces on initialization
        self.reload_faces()

    def reload_faces(self):
        """Reloads all known faces from the directory."""
        self.known_encodings = []
        self.known_names = []
        self.load_known_faces()

    def load_known_faces(self):
        """Load images from known_faces directory (and subdirectories) and encode them."""
        print(f"[*] Loading known faces from '{self.known_faces_dir}'...")
        
        if not os.path.exists(self.known_faces_dir):
            os.makedirs(self.known_faces_dir)
            print(f"[!] Created directory '{self.known_faces_dir}'.")
            return

        # Handle both flat files and subdirectories
        for entry in os.listdir(self.known_faces_dir):
            entry_path = os.path.join(self.known_faces_dir, entry)
            
            if os.path.isdir(entry_path):
                # It's a person's folder
                person_name = entry
                for image_name in os.listdir(entry_path):
                    if image_name.lower().endswith((".jpg", ".jpeg", ".png")):
                        self._process_image(os.path.join(entry_path, image_name), person_name)
            
            elif os.path.isfile(entry_path) and entry.lower().endswith((".jpg", ".jpeg", ".png")):
                # Legacy support: flat file where filename is name
                person_name = os.path.splitext(entry)[0]
                self._process_image(entry_path, person_name)

        print(f"[*] Total known faces loaded: {len(self.known_names)} (from {len(set(self.known_names))} unique people)")

    def _process_image(self, image_path, name):
        """Helper to encode a single image file."""
        try:
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            
            if len(encodings) > 0:
                # We can store multiple encodings for the same person from different images
                for encoding in encodings:
                    self.known_encodings.append(encoding)
                    self.known_names.append(name)
                # print(f"[+] Loaded: {name} from {os.path.basename(image_path)}")
            else:
                print(f"[?] No face found in {image_path}")
        except Exception as e:
            print(f"[!] Error loading {image_path}: {e}")

    def register_new_face(self, frame, name):
        """
        Save the frame as a new known face for the given name.
        Creates a subdirectory for the name if it doesn't exist.
        """
        if not name:
            return False, "Name cannot be empty."

        person_dir = os.path.join(self.known_faces_dir, name)
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.jpg"
        image_path = os.path.join(person_dir, filename)
        
        # Save the frame
        cv2.imwrite(image_path, frame)
        
        # Encode and add to memory immediately
        try:
            # Re-read from disk to ensure consistency or just use the frame
            # Using face_recognition.load_image_file is safer as it converts to RGB/standardizes
            new_image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(new_image)
            
            if not encodings:
                os.remove(image_path) # Clean up if no face
                return False, "No face detected in the captured image."

            self.known_encodings.append(encodings[0])
            self.known_names.append(name)
            return True, f"Success! {name} registered."
        except Exception as e:
            return False, f"Error encoding face: {e}"

    def recognize_faces(self, frame):
        """
        Process a frame and return locations and names.
        """
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding, tolerance=self.tolerance)
            name = "Unknown"

            face_distances = face_recognition.face_distance(self.known_encodings, face_encoding)
            if len(face_distances) > 0:
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_names[best_match_index]

            face_names.append(name)
            
        return face_locations, face_names

    def get_registered_users(self):
        """Return a list of unique registered names."""
        return sorted(list(set(self.known_names)))

    def delete_user(self, name):
        """Delete all data for a user."""
        person_dir = os.path.join(self.known_faces_dir, name)
        if os.path.exists(person_dir):
            shutil.rmtree(person_dir)
            self.reload_faces()
            return True
        # Check flat file legacy
        legacy_file = os.path.join(self.known_faces_dir, f"{name}.jpg")
        if os.path.exists(legacy_file):
            os.remove(legacy_file)
            self.reload_faces()
            return True
        return False

# Legacy run method for backward compatibility / testing
def run_legacy_cli_mode():
    system = FaceRecognitionSystem()
    video_capture = cv2.VideoCapture(0)
    
    if not video_capture.isOpened():
        print("[!] Error: Could not open webcam.")
        return

    print("[*] Starting Legacy CLI Recognition...")
    print("    - Press 'q' to quit")
    print("    - Press 's' to save (CLI input required)")

    process_current_frame = True
    face_locations = []
    face_names = []

    while True:
        ret, frame = video_capture.read()
        if not ret: break

        if process_current_frame:
            face_locations, face_names = system.recognize_faces(frame)

        process_current_frame = not process_current_frame

        # Display results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

        cv2.imshow('Face Recognition CLI', frame)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s'):
            # This legacy input will pause the video stream in the GUI loop which is not ideal
            # but this is just for the backup CLI mode
            name = input("Enter name: ")
            success, msg = system.register_new_face(frame, name)
            print(msg)

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_legacy_cli_mode()
