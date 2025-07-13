# ===================================================================
# Python Code: ArUco Follower with Wireless Control via ESP32
# ===================================================================

# Import the OpenCV library for computer vision (for webcam and ArUco detection)
import cv2
# Import NumPy for numerical operations, especially with arrays (used in image processing)
import numpy as np
# Import socket for network communication with ESP32
import socket
# Import time for delays (e.g., for connection attempts, or if needed elsewhere)
import time

# --- ESP32 Connection Configuration ---
# IMPORTANT:
# 1. Replace with the ACTUAL IP address shown in your ESP32's Serial Monitor
#    after it connects to your WiFi network.
# 2. Ensure your laptop and ESP32 are on the SAME WiFi network.
#    >>> MAKE SURE THIS MATCHES YOUR ESP32'S CURRENT IP! <<<
ESP32_IP = "10.248.244.54" # <<< I've set this back to the IP from your previous output. CONFIRM THIS!
ESP32_PORT = 80         # This must match the port specified in the ESP32 code (WiFiServer server(80);)

# Global socket object for communication
esp32_socket = None

try:
    # Attempt to establish connection to the ESP32
    esp32_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    esp32_socket.settimeout(5) # Set a timeout for connection attempts (5 seconds)
    esp32_socket.connect((ESP32_IP, ESP32_PORT))
    esp32_socket.settimeout(None) # Remove timeout after successful connection for continuous operation
    print(f"Connected to ESP32 at {ESP32_IP}:{ESP32_PORT}")
    time.sleep(1) # Give a moment for connection to stabilize
except socket.error as e:
    print(f"Could not connect to ESP32: {e}.")
    print(f"Please check: 1. Is ESP32 powered and running the server sketch? 2. Is ESP32_IP '{ESP32_IP}' correct?")
    print("3. Are laptop and ESP32 on the same Wi-Fi? 4. Is firewall blocking port 80?")
    esp32_socket = None # Set to None if connection fails
except Exception as e:
    print(f"An unexpected error occurred during connection: {e}")
    esp32_socket = None

# --- ArUco Dictionary Setup ---
ARUCO_DICT = cv2.aruco.DICT_6X6_250
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
arucoParams = cv2.aruco.DetectorParameters()
detector = cv2.aruco.ArucoDetector(arucoDict, arucoParams)

# --- Configuration for Following Logic ---
TARGET_MARKER_ID = 25
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
CENTER_ZONE_THRESHOLD = 0.15 # Percentage of frame width for the center "dead zone"
IDEAL_MARKER_AREA_MIN = 3000 # Min pixel area for marker at ideal distance
IDEAL_MARKER_AREA_MAX = 5000 # Max pixel area for marker at ideal distance
TOO_CLOSE_AREA_THRESHOLD = 6000 # If marker area is above this, it's too close
TOO_FAR_AREA_THRESHOLD = 1500  # If marker area is below this, it's too far

# --- Webcam Setup ---
url="http://10.248.244.181:8080/video"
cap = cv2.VideoCapture(0) # 0 for default webcam, change if you have multiple
cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

if not cap.isOpened():
    print("Error: Could not open video stream. Please check your camera connection and drivers.")
    exit() # Exit the script if webcam cannot be opened

print("ArUco Follower (Wireless via ESP32) is running.")
print("Press 'q' to quit the program at any time.")
current_movement_state = 'S' # S: Stop, F: Forward, L: Left, R: Right, B: Back


def set_motor_state(state):
    """
    Controls the motors by sending commands wirelessly to the ESP32.
    """
    global current_movement_state
    global esp32_socket # Ensure we can modify the global socket object

    if esp32_socket is None: # If ESP32 connection was not established or lost, do nothing
        return

    # Only send command if the state has changed, to reduce network traffic.
    if state == current_movement_state:
        return

    try:
        # Encode the state character to bytes and send it
        esp32_socket.sendall(state.encode('utf-8'))
        print(f"Sent command: {state}")
        current_movement_state = state # Update the last sent state after command is issued
    except socket.error as e:
        print(f"Error sending command to ESP32: {e}")
        esp32_socket = None # Mark as disconnected
        # For simplicity, we'll just stop trying until the script is restarted
        # or you implement a more robust reconnection loop outside this function.
    except Exception as e:
        print(f"An unexpected error occurred while sending command: {e}")
        esp32_socket = None


# --- Main Loop for ArUco Detection and Robot Control ---
while True:
    ret, frame = cap.read() # Read a frame from the webcam
    if not ret:
        print("Failed to grab frame. Exiting...")
        break # Exit loop if frame cannot be read

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert frame to grayscale for ArUco detection

    # Detect ArUco markers in the grayscale frame
    corners, ids, rejected = detector.detectMarkers(gray)

    command_to_send = 'S' # Default command is stop

    if ids is not None:
        ids = ids.flatten() # Flatten the ids array for easier processing

        if TARGET_MARKER_ID in ids:
            # Find the index of our target marker
            target_marker_index = np.where(ids == TARGET_MARKER_ID)[0][0]
            # Get the corners of the target marker
            target_corners_for_drawing = corners[target_marker_index]

            # Draw the detected target marker on the frame
            cv2.aruco.drawDetectedMarkers(frame, [target_corners_for_drawing], np.array([[TARGET_MARKER_ID]]))

            # Calculate the center (cX, cY) of the target marker
            M = cv2.moments(target_corners_for_drawing[0])
            if M["m00"] != 0: # Avoid division by zero
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])

                # Draw a circle at the center and display ID/Area
                cv2.circle(frame, (cX, cY), 5, (0, 255, 0), -1) # Green circle
                cv2.putText(frame, f"ID: {TARGET_MARKER_ID}", (cX - 40, cY - 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) # White text

                marker_area = cv2.contourArea(target_corners_for_drawing[0]) # Calculate the area of the marker
                cv2.putText(frame, f"Area: {int(marker_area)}", (cX - 40, cY + 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2) # White text

                # --- Decision Logic for Following ---
                # Check distance first (based on marker area)
                if marker_area > TOO_CLOSE_AREA_THRESHOLD:
                    # Marker is too close, stop the robot
                    command_to_send = 'S'
                    cv2.putText(frame, "STATUS: TOO CLOSE", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2) # Red

                elif marker_area < TOO_FAR_AREA_THRESHOLD:
                    # Marker is too far, move forward and adjust direction
                    center_x_frame = FRAME_WIDTH // 2
                    right_boundary = center_x_frame - (FRAME_WIDTH * CENTER_ZONE_THRESHOLD / 2)
                    left_boundary = center_x_frame + (FRAME_WIDTH * CENTER_ZONE_THRESHOLD / 2)

                    cv2.line(frame, (int(left_boundary), 0), (int(left_boundary), FRAME_HEIGHT), (255, 0, 0), 2) # Blue lines
                    cv2.line(frame, (int(right_boundary), 0), (int(right_boundary), FRAME_HEIGHT), (255, 0, 0), 2)

                    if cX < left_boundary:
                        command_to_send = 'L' # Turn left
                        cv2.putText(frame, "STATUS: TOO FAR, TURNING LEFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2) # Yellow
                    elif cX > right_boundary:
                        command_to_send = 'R' # Turn right
                        cv2.putText(frame, "STATUS: TOO FAR, TURNING RIGHT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2) # Yellow
                    else:
                        command_to_send = 'F' # Move forward (centered)
                        cv2.putText(frame, "STATUS: TOO FAR, MOVING FORWARD", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2) # Green

                else: # Marker is within IDEAL_MARKER_AREA_MIN and IDEAL_MARKER_AREA_MAX
                    # At ideal distance, now adjust horizontally or move gently forward
                    center_x_frame = FRAME_WIDTH // 2
                    left_boundary = center_x_frame - (FRAME_WIDTH * CENTER_ZONE_THRESHOLD / 2)
                    right_boundary = center_x_frame + (FRAME_WIDTH * CENTER_ZONE_THRESHOLD / 2)

                    cv2.line(frame, (int(left_boundary), 0), (int(left_boundary), FRAME_HEIGHT), (255, 0, 0), 2) # Blue lines
                    cv2.line(frame, (int(right_boundary), 0), (int(right_boundary), FRAME_HEIGHT), (255, 0, 0), 2)

                    if cX < left_boundary:
                        command_to_send = 'L' # Turn left to center
                        cv2.putText(frame, "STATUS: IDEAL DISTANCE, TURNING LEFT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    elif cX > right_boundary:
                        command_to_send = 'R' # Turn right to center
                        cv2.putText(frame, "STATUS: IDEAL DISTANCE, TURNING RIGHT", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    else:
                        command_to_send = 'S' # Stop
                        cv2.putText(frame, "STATUS: IDEAL DISTANCE, CENTERED, STOP", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 2) # Magenta

        else: # Target marker ID is not found (but other markers might be present)
            command_to_send = 'S' # Stop
            cv2.putText(frame, "STATUS: TARGET MARKER NOT FOUND", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
    else: # No markers detected at all
        command_to_send = 'S' # Stop
        cv2.putText(frame, "STATUS: NO MARKERS DETECTED", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Send the determined command to the ESP32 wirelessly.
    set_motor_state(command_to_send)

    cv2.imshow("ArUco Follower (Trolley Cam) - Wireless", frame) # Display the video feed

    if cv2.waitKey(1) & 0xFF == ord('q'): # Press 'q' to quit
        break

# --- Cleanup ---
cap.release() # Release the webcam
cv2.destroyAllWindows() # Close all OpenCV windows
# Close the socket connection if it was established
if esp32_socket:
    esp32_socket.close()
    print("Wireless connection closed.")