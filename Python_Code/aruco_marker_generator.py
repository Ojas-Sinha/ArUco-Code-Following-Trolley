# Import the OpenCV library
import cv2
# Import NumPy for array operations
import numpy as np

# Define the dictionary for the ArUco markers
# ARUCO_DICT = cv2.aruco.DICT_6X6_50 is a common choice, meaning 6x6 bit markers with 50 possible IDs
ARUCO_DICT = cv2.aruco.DICT_6X6_250 # Using 250 possible IDs for more variety
arucoDict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)

# Define the ID for the marker you want to generate
# Let's say we want to generate a marker with ID 25
marker_id = 25


# Define the size of the marker image in pixels
# A size of 200x200 pixels is good for printing
marker_size = 200

# Create an empty image (white background) to draw the marker on
# It's good practice to add a border around the marker
border_size = 50 # Pixels for the border
total_size = marker_size + 2 * border_size
marker_image = np.full((total_size, total_size), 255, dtype=np.uint8) # White background

# Generate the ArUco marker
# The marker is drawn onto the empty image at the specified coordinates
# The last argument is the border bits (1 or 2 are common)
cv2.aruco.generateImageMarker(arucoDict, marker_id, marker_size, marker_image[border_size:border_size+marker_size, border_size:border_size+marker_size], 1)

# Save the generated marker image to a file
# The filename will include the ID for easy identification
filename = f"aruco_marker_{marker_id}.png"
cv2.imwrite(filename, marker_image)

print(f"ArUco marker with ID {marker_id} generated and saved as {filename}")
print("You can print this image and use it as your physical ArUco marker.")