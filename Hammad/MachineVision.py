import cv2
import numpy as np

direction = []
# Panels list to hold detected panel positions
def nothing(x):
    pass

# Load the image
image_path = 'H:\\captures\\picCamTow (1).png'
image = cv2.imread(image_path)

# Ensure image is loaded
if image is None:
    print(f"Error loading image at {image_path}")
    exit()

blurImg = cv2.bilateralFilter(image, 20, 75, 75)

# Convert the image from BGR to HSV color space
hsv_image = cv2.cvtColor(blurImg, cv2.COLOR_BGR2HSV)

# Create a window for trackbars
cv2.namedWindow('Trackbars')

# Create trackbars for HSV range adjustments
cv2.createTrackbar('Hue Low', 'Trackbars', 0, 179, nothing)
cv2.createTrackbar('Sat Low', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Val Low', 'Trackbars', 0, 255, nothing)
cv2.createTrackbar('Hue High', 'Trackbars', 179, 179, nothing)
cv2.createTrackbar('Sat High', 'Trackbars', 255, 255, nothing)
cv2.createTrackbar('Val High', 'Trackbars', 255, 255, nothing)

# Function to set sliders based on color
def set_sliders(color):
    if color == 'red':
        cv2.setTrackbarPos('Hue Low', 'Trackbars', 0)
        cv2.setTrackbarPos('Hue High', 'Trackbars', 179)
        cv2.setTrackbarPos('Sat Low', 'Trackbars', 206)
        cv2.setTrackbarPos('Sat High', 'Trackbars', 255)
        cv2.setTrackbarPos('Val Low', 'Trackbars', 0)
        cv2.setTrackbarPos('Val High', 'Trackbars', 118)

    elif color == 'blue':
        cv2.setTrackbarPos('Hue Low', 'Trackbars', 110)
        cv2.setTrackbarPos('Hue High', 'Trackbars', 140)
        cv2.setTrackbarPos('Sat Low', 'Trackbars', 100)
        cv2.setTrackbarPos('Sat High', 'Trackbars', 255)
        cv2.setTrackbarPos('Val Low', 'Trackbars', 100)
        cv2.setTrackbarPos('Val High', 'Trackbars', 255)

    elif color == 'green':
        cv2.setTrackbarPos('Hue Low', 'Trackbars', 25)
        cv2.setTrackbarPos('Hue High', 'Trackbars', 106)
        cv2.setTrackbarPos('Sat Low', 'Trackbars', 146)
        cv2.setTrackbarPos('Sat High', 'Trackbars', 216)
        cv2.setTrackbarPos('Val Low', 'Trackbars', 86)
        cv2.setTrackbarPos('Val High', 'Trackbars', 212)

    elif color == 'yellow':
        cv2.setTrackbarPos('Hue Low', 'Trackbars', 24)
        cv2.setTrackbarPos('Hue High', 'Trackbars', 57)
        cv2.setTrackbarPos('Sat Low', 'Trackbars', 65)
        cv2.setTrackbarPos('Sat High', 'Trackbars', 255)
        cv2.setTrackbarPos('Val Low', 'Trackbars', 145)
        cv2.setTrackbarPos('Val High', 'Trackbars', 230)

    elif color == 'maroon':
        cv2.setTrackbarPos('Hue Low', 'Trackbars', 0)
        cv2.setTrackbarPos('Hue High', 'Trackbars', 10)
        cv2.setTrackbarPos('Sat Low', 'Trackbars', 50)
        cv2.setTrackbarPos('Sat High', 'Trackbars', 255)
        cv2.setTrackbarPos('Val Low', 'Trackbars', 50)
        cv2.setTrackbarPos('Val High', 'Trackbars', 255)

# Initialize flags
color_changed = True
initial_run = True

while True:
    # Reset Panels list for each loop iteration
    Panels = []

    # Get current positions of the trackbars
    hue_low = cv2.getTrackbarPos('Hue Low', 'Trackbars')
    sat_low = cv2.getTrackbarPos('Sat Low', 'Trackbars')
    val_low = cv2.getTrackbarPos('Val Low', 'Trackbars')
    hue_high = cv2.getTrackbarPos('Hue High', 'Trackbars')
    sat_high = cv2.getTrackbarPos('Sat High', 'Trackbars')
    val_high = cv2.getTrackbarPos('Val High', 'Trackbars')

    # Define color range based on trackbar positions
    lower_bound = np.array([hue_low, sat_low, val_low])
    upper_bound = np.array([hue_high, sat_high, val_high])

    # Create mask using the HSV range
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)

    # Apply morphological operations to remove small specks
    kernel = np.ones((5, 5), np.uint8)
    cleaned_mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    min_area = 500
    max_area = 7850

    height, width = image.shape[:2]
    # Draw contours on a copy of the original image
    contour_image = image.copy()

    bottom_half = height // 2

    sec = []
    for i in range(8):
        sec.append((i + 1) * (width / 8))

    # Find contours in the cleaned mask
    contours, _ = cv2.findContours(cleaned_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        area = cv2.contourArea(contour)
        if min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(contour)
            if y > bottom_half:
                Panels.append(x)
                cv2.rectangle(contour_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                Panels.sort()

    # Determine panel direction
    panel_directions = []
    for panel in Panels:
        if 0 < panel < sec[0]:
            panel_directions.append("LL")
        elif sec[0] < panel < sec[1]:
            panel_directions.append("LR")
        elif sec[1] < panel < sec[2]:
            panel_directions.append("RL")
        elif sec[2] < panel < sec[3]:
            panel_directions.append("RR")
        elif sec[3] < panel < sec[4]:
            panel_directions.append("RR")
        elif sec[4] < panel < sec[5]:
            panel_directions.append("RL")
        elif sec[5] < panel < sec[6]:
            panel_directions.append("LR")
        elif sec[6] < panel < sec[7]:
            panel_directions.append("LL")

    # Print directions if needed
    if color_changed or initial_run:
        if panel_directions:  # Ensure there is something to print
            print("\n".join(panel_directions) + "\n")
        color_changed = False
        initial_run = False

    # Display the images
    cv2.imshow('Original Image', image)
    cv2.imshow('Blurred Image', blurImg)
    cv2.imshow('Mask', cleaned_mask)
    cv2.imshow('Contours', contour_image)

    # Check for key presses to change color
    key = cv2.waitKey(30) & 0xFF
    if key == ord('r'):
        set_sliders('red')
        color_changed = True
    elif key == ord('b'):
        set_sliders('blue')
        color_changed = True
    elif key == ord('g'):
        set_sliders('green')
        color_changed = True
    elif key == ord('y'):
        set_sliders('yellow')
        color_changed = True
    elif key == ord('m'):
        set_sliders('maroon')
        color_changed = True
    elif key == ord('q'):
        break

# Clean up
cv2.destroyAllWindows()
