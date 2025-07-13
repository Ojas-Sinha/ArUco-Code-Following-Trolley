# **ArUco Code Following Trolley**

This project implements an **ArUco Code Following Trolley** using **ESP32**, **OpenCV**, and **wireless communication**.  
The trolley detects a specific ArUco marker and follows it by adjusting motor movements accordingly.

---

## **Features**

- ArUco marker-based object tracking using OpenCV.
- Wireless control of ESP32 via WiFi (TCP socket communication).
- Motor control using L298N Motor Driver (manages direction, speed, and heat dissipation).
- Real-time decision-making: Forward, Left, Right, Stop.
- Marker generator for generating new ArUco codes for different IDs.

---

## **Hardware Used**

- ESP32 Dev Board
- L298N Motor Driver Module (with heat sink for thermal management)
- BO Motors with Wheels
- Power Supply (Battery)
- Laptop Webcam or Mobile IP Webcam (for remote video feed)

---

## **Software Components**

### **Python Side (Laptop)**

| File | Description |
|---|---|
| `aruco_follower_wireless.py` | Detects ArUco marker and sends movement commands to ESP32 wirelessly |
| `aruco_marker_generator.py` | Generates an ArUco marker image (default ID 25) for printing |

---

### **ESP32 Side**

| File | Description |
|---|---|
| `ESP32_Motor_Control.ino` | Receives wireless TCP commands and controls motors using L298N |

---

## **Setup Instructions**

### **1️⃣ Install Python Requirements**

```bash
pip install opencv-python numpy
```
For ArUco detection, OpenCV must include cv2.aruco.
If not available, install:
```bash
pip install opencv-contrib-python
```
### **2️⃣ Upload ESP32 Code**
- Open ESP32_Motor_Control.ino in Arduino IDE.
- Connect the ESP32 to your computer.
- Replace the WiFi SSID and Password in the code with your credentials.
- Upload the code to ESP32.
- Open the Serial Monitor to note the ESP32 IP Address.
- Ensure the Python code uses the same IP.
### **3️⃣ Run Python Code**
Generate ArUco Marker
```bash
python aruco_marker_generator.py
```
- Generates a 6x6 ArUco marker with ID: 25
- Output: aruco_marker_25.png
- Print this marker and attach it to the object/person to follow.

Run the Follower Program
```bash
python aruco_follower_wireless.py
```
This code captures live video, detects the marker, and sends control signals to ESP32 over WiFi.

## **Movement Logic**
| ArUco Marker Position | Trolley Action |
|---|---|
|Marker too close|	Stop|
|Marker too far (centered)|	Move Forward|
|Marker on the left side|	Turn Left|
|Marker on the right side|	Turn Right|

## **Marker Used**
- Type: 6x6 ArUco Marker
- ID: 25
- Output File: aruco_marker_25.png

## **Advantages**
- Wireless operation (no USB tethering required between laptop and trolley).
- OpenCV-based tracking ensures accurate and fast object detection.
- Customizable marker generation allows easy setup for different use cases.
- L298N motor driver manages both direction and speed control while handling motor heat efficiently.

## **Applications**
- Smart Shopping Cart
- Warehouse Trolley Automation
- Surveillance Robots
- Person Follower Robots
