# ArUco Code Following Trolley

This project implements a **ArUco Code Following Trolley** using **ESP32**, **OpenCV**, and **wireless communication**.  
The trolley detects a specific ArUco marker and follows it by adjusting motor movements accordingly.

## Features

- ArUco marker-based object tracking using OpenCV.
- Wireless control of ESP32 via WiFi (TCP socket communication).
- Motor control using L298N Motor Driver.
- Real-time decision-making: Forward, Left, Right, Stop.
- Marker generator for generating new QR/ArUco codes.

---

## Hardware Used

- ESP32 Dev Board
- L298N Motor Driver Module (with heat sink for thermal management)
- BO Motors with Wheels
- Power Supply (Battery)
- Laptop Webcam or Mobile IP Webcam (optional for remote feed)

---

## Software Components

### Python Side (Laptop)

| File | Description |
|---|---|
| `aruco_follower_wireless.py` | Detects ArUco marker and sends movement commands to ESP32 |
| `aruco_marker_generator.py` | Generates an ArUco marker image (ID 25) for printing |

---

### ESP32 Side

| File | Description |
|---|---|
| `ESP32_Motor_Control.ino` | Listens to TCP commands and controls motors accordingly |

---

## Setup Instructions

### 1️⃣ Install Python Requirements

```bash
pip install opencv-python numpy
