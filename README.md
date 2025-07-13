Project Overview
The ArUco Code Following Trolley is a wireless robot system that follows a person carrying a specific ArUco marker.
The project uses computer vision (OpenCV) for marker detection and sends wireless control signals to an ESP32 for motor operation.
It eliminates the need for physical line-following and enables dynamic human tracking using marker recognition.

Key Features
ArUco Marker Tracking using OpenCV

Wireless Motor Control via ESP32 (WiFi TCP Sockets)

L298N Motor Driver for Motor Management

Dynamic Distance and Direction Adjustment

Real-Time Video Feed Processing

Components Used
ESP32 Development Board

L298N Motor Driver Module (with heat management via heat sinks)

2 × BO Motors with Wheels

Battery for Motor Power

Laptop Webcam or IP Webcam (for video input)

OpenCV & Python for image processing

Project Structure
File	Description
aruco_follower_wireless.py	Python script for ArUco detection and wireless command sending to ESP32
ESP32_Motor_Control.ino	Arduino code for ESP32 to control L298N motor driver over WiFi
aruco_marker_generator.py	Python script to generate ArUco markers (ID 25 used in this project)
aruco_marker_25.png	Sample generated ArUco marker (ID 25)
README.md	Project documentation

How It Works
Marker Generation:
Use aruco_marker_generator.py to create a unique marker with a specific ID (e.g., 25).
Print this marker and attach it to the object/person the trolley will follow.

Laptop Side (Python):

Captures video using OpenCV.

Detects the marker and determines distance & angle.

Sends movement commands (F, B, L, R, S) to ESP32 over WiFi.

ESP32 Side (Arduino):

Listens for TCP commands on port 80.

Controls motor direction using L298N based on received commands.

Setup Instructions
ESP32
Upload ESP32_Motor_Control.ino to ESP32 using Arduino IDE.

Configure your WiFi SSID & Password in the code.

Connect ESP32 to L298N Motor Driver as per the following pin mapping:

ESP32 Pin	L298N Input
25	IN1
26	IN2
27	IN3
14	IN4

Laptop (Python)
Install dependencies:

bash
Copy
Edit
pip install opencv-python numpy
Run the main follower script:

bash
Copy
Edit
python aruco_follower_wireless.py
Use the generated ArUco marker (ID 25) for testing.

Controls
Command Sent	Action
F	Move Forward
B	Move Backward
L	Turn Left
R	Turn Right
S	Stop

Advantages
Contactless Tracking:
Tracks a person without needing line-following tracks.

Wireless Control:
No wired connection between laptop and motors; control via TCP.

L298N Efficiency:
Handles both forward and reverse motion with built-in heat sinks for thermal management.

Flexible Deployment:
Works indoors for material handling, shopping carts, personal trolleys, etc.

Applications
Smart Shopping Trolley

Surveillance & Security Robots

Autonomous Indoor Delivery Systems

Personal Assistance Robots

Screenshots
Marker Example	Live Tracking
(Add video/image here if needed)

Acknowledgments
This project was developed during the Robomanthan Internship Program as part of a learning initiative in Robotics, AI, and IoT.

