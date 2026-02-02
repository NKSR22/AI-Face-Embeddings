# IoT Hardware & ESP32 Integration

This guide explains how to set up the ESP32 hardware to work with the CORTEX Face Recognition system.

## 🛠️ Required Components
- **ESP32 Development Board** (e.g., ESP32-WROOM-32)
- **Relay Module** (5V or 3.3V Trigger)
- **12V Solenoid Door Lock**
- **External 12V Power Supply** (for the lock)
- **Jumper Wires**

## 🔌 Wiring Diagram
```mermaid
graph LR
    subgraph "Computer (Face AI)"
        PC[Python App]
    end
    
    subgraph "ESP32 (WiFi Controller)"
        PC -.->|WiFi / HTTP| ESP[ESP32]
        ESP -->|GPIO 4| RELAY[Relay Module]
    end
    
    subgraph "Hardware Block"
        RELAY -->|Switch| LOCK[12V Solenoid Lock]
        POW[12V Adapter] --- LOCK
        POW --- RELAY
    end
```

## 💻 ESP32 Source Code (Arduino IDE)
Copy this code to your Arduino IDE, update your WiFi credentials, and upload it to your ESP32.

```cpp
#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WebServer server(80);
const int relayPin = 4; // GPIO Pin connected to Relay

void handleUnlock() {
  Serial.println("Unlock Triggered!");
  digitalWrite(relayPin, LOW); // Trigger Relay (Active Low)
  server.send(200, "text/plain", "Unlocked");
  
  delay(3000); // Keep unlocked for 3 seconds
  
  digitalWrite(relayPin, HIGH); // Lock again
  Serial.println("Locked");
}

void setup() {
  Serial.begin(115200);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Default Locked

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi Connected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  server.on("/unlock", handleUnlock);
  server.begin();
}

void loop() {
  server.handleClient();
}
```

## ⚙️ Configuration
1. Note the **IP Address** shown in the Arduino Serial Monitor.
2. Open the Python GUI.
3. Enter the IP address in the **IoT / WiFi Control** panel.
4. Enable the **IoT Trigger**.
