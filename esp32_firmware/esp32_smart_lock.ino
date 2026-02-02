/*
 * CORTEX Smart Lock - ESP32 Firmware
 * Developed by: อาจารย์นครินทร์ ศรีปัญญา
 * 
 * Description: 
 * This firmware connects to WiFi and listens for an HTTP GET request on /unlock.
 * Once triggered, it activates a relay to open a solenoid lock.
 */

#include <WiFi.h>
#include <WebServer.h>

// --- Configuration ---
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WebServer server(80);
const int relayPin = 4; // GPIO Pin connected to Relay (Adjust as needed)
const int unlockDuration = 3000; // Time in milliseconds to keep the door unlocked

// --- Handlers ---
void handleRoot() {
  server.send(200, "text/plain", "CORTEX ESP32 IoT Node is Online.");
}

void handleUnlock() {
  Serial.println("[IoT] Unlock Triggered from Python App");
  
  // Trigger Relay (Assuming Active Low Relay)
  digitalWrite(relayPin, LOW); 
  server.send(200, "text/plain", "OK: Door Unlocked");
  
  delay(unlockDuration);
  
  // Return to Locked state
  digitalWrite(relayPin, HIGH); 
  Serial.println("[IoT] Locked");
}

void handleNotFound() {
  server.send(404, "text/plain", "Not Found");
}

void setup() {
  Serial.begin(115200);
  
  // Setup Relay Pin
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Default state is locked (Relay OFF)

  // Connect to WiFi
  Serial.println();
  Serial.print("[WiFi] Connecting to ");
  Serial.println(ssid);
  
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n[WiFi] Connected Successfully!");
    Serial.print("[WiFi] IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n[WiFi] Failed to connect. Please check your credentials.");
  }

  // Define API Routes
  server.on("/", handleRoot);
  server.on("/unlock", handleUnlock);
  server.onNotFound(handleNotFound);

  // Start Server
  server.begin();
  Serial.println("[HTTP] Server started on port 80");
}

void loop() {
  server.handleClient();
  
  // Optional: Connection Watchdog
  if (WiFi.status() != WL_CONNECTED) {
    // Attempt reconnection if lost
    static unsigned long lastReconnect = 0;
    if (millis() - lastReconnect > 10000) {
      Serial.println("[WiFi] Connection lost. Reconnecting...");
      WiFi.begin(ssid, password);
      lastReconnect = millis();
    }
  }
}
