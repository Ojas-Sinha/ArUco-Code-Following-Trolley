/*
  ArUco Code Following Trolley - ESP32 Motor Control
  This program connects ESP32 to WiFi, sets up a TCP server, and controls the motors via L298N based on commands from Python.
*/

#include <WiFi.h>

// --- WiFi Setup ---
const char* ssid = "xxxxxxxxx";  // Your WiFi SSID
const char* password = "xxxxxxxxx";  // Your WiFi Password

// --- Motor Pins connected to L298N Motor Driver ---
const int IN1_PIN = 25;  // Left Motor Forward
const int IN2_PIN = 26;  // Left Motor Backward
const int IN3_PIN = 27;  // Right Motor Forward
const int IN4_PIN = 14;  // Right Motor Backward

WiFiServer server(80);  // Create TCP server on port 80

void setup() {
  Serial.begin(115200);
  delay(100);

  // Set motor control pins as OUTPUT
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  pinMode(IN3_PIN, OUTPUT);
  pinMode(IN4_PIN, OUTPUT);

  // Connect to WiFi
  Serial.print("Connecting to WiFi ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  int connect_attempts = 0;
  while (WiFi.status() != WL_CONNECTED && connect_attempts < 20) { // Try connecting for ~10 seconds
    delay(500);
    Serial.print(".");
    connect_attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi connected!");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
    server.begin();  // Start listening for client connections
    Serial.println("Server started.");
  } else {
    Serial.println("\nFailed to connect to WiFi.");
  }
}

// --- Function to control motor directions ---
void setMotorState(char state) {
  // Turn off all motors first for safety
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  digitalWrite(IN3_PIN, LOW);
  digitalWrite(IN4_PIN, LOW);
  delay(10);  // Short delay to avoid glitches

  // Control logic based on received character
  if (state == 'F') {  // Forward
    digitalWrite(IN1_PIN, HIGH);
    digitalWrite(IN3_PIN, HIGH);
    Serial.println("Motors: FORWARD");
  } else if (state == 'B') {  // Backward
    digitalWrite(IN2_PIN, HIGH);
    digitalWrite(IN4_PIN, HIGH);
    Serial.println("Motors: BACKWARD");
  } else if (state == 'L') {  // Turn Left
    digitalWrite(IN2_PIN, HIGH);  // Left wheel backward
    digitalWrite(IN3_PIN, HIGH);  // Right wheel forward
    Serial.println("Motors: LEFT");
  } else if (state == 'R') {  // Turn Right
    digitalWrite(IN1_PIN, HIGH);  // Left wheel forward
    digitalWrite(IN4_PIN, HIGH);  // Right wheel backward
    Serial.println("Motors: RIGHT");
  } else if (state == 'S') {  // Stop
    Serial.println("Motors: STOP");
  }
}

void loop() {
  // Accept new client connection
  WiFiClient client = server.available();

  if (client) {
    Serial.println("Client connected.");

    // Stay connected while the client is active
    while (client.connected()) {
      if (client.available()) {
        char command = client.read();  // Read single character command
        Serial.print("Received command: ");
        Serial.println(command);
        setMotorState(command);  // Control motors
      }
      delay(1);  // Avoid tight loop
    }
    Serial.println("Client disconnected.");
  }
}