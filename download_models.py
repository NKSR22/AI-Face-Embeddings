import os
import urllib.request

def download_file(url, filename):
    if os.path.exists(filename):
        print(f"[*] {filename} already exists. Skipping download.")
        return
    
    print(f"[*] Downloading {filename} from {url}...")
    try:
        urllib.request.urlretrieve(url, filename)
        print(f"[+] Downloaded {filename} successfully.")
    except Exception as e:
        print(f"[!] Error downloading {filename}: {e}")

if __name__ == "__main__":
    # Project directory
    base_path = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(base_path, "models")
    
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)
        print(f"[*] Created directory '{model_dir}'.")

    # YuNet (Face Detection)
    yunet_url = "https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
    yunet_path = os.path.join(model_dir, "face_detection_yunet_2023mar.onnx")
    
    # SFace (Face Recognition)
    sface_url = "https://github.com/opencv/opencv_zoo/raw/refs/heads/main/models/face_recognition_sface/face_recognition_sface_2021dec.onnx"
    sface_path = os.path.join(model_dir, "face_recognition_sface_2021dec.onnx")

    download_file(yunet_url, yunet_path)
    download_file(sface_url, sface_path)

    print("\n[*] Model setup complete.")
