# Lab Manual: AI Face Recognition & IoT Control

## Objective
To understand the workflow of a modern face recognition system and its integration with IoT devices via WiFi.

## Prerequisites
- Computer with Python installed.
- Webcam.
- ESP32 (Optional, for IoT section).

## Step-by-Step Experiment

### 1. Model Deployment
1. Install dependencies using `pip install -r requirements.txt`.
2. Execute `python download_models.py` and observe the ONNX model files in the `models/` folder.
3. **Question**: Why do we use ONNX instead of raw Python code for models?

### 2. Face Registration
1. Run `python gui.py`.
2. Register your face using the **CAPTURE FACE** button.
3. Observe how a new folder is created inside `known_faces/`.

### 3. Face Identification
1. Show your face to the camera.
2. Observe the green/red bounding boxes and the identification results.
3. Test with different lighting conditions and angles.

### 4. IoT Integration (The "Smart Lock" Concept)
1. Enter the IP address of your ESP32 in the IoT panel.
2. Toggle the **ENABLE IoT TRIGGER**.
3. Observe the Logs when a match is found.
4. **Task**: Explain how the "Cooldown" mechanism helps save resources and prevents hardware stress.

### 5. Hardware Implementation (Final Lab)
1. Refer to [HARDWARE.md](HARDWARE.md) for the wiring diagram.
2. Flash the provided Arduino code to your ESP32.
3. Connect the Relay and Solenoid Lock according to the schematic.
4. **Test**: Use the **TEST UNLOCK** button in the Python app and verify the Solenoid Lock physically clicks open.

## Discussion
- How does the system handle "Unknown" people?
- What are the privacy implications of running this system locally vs. on the cloud?
