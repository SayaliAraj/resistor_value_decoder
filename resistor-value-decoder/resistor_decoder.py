import cv2
import numpy as np

# Define color code mappings for resistor values
COLOR_CODES = {
    'black': 0,
    'brown': 1,
    'red': 2,
    'orange': 3,
    'yellow': 4,
    'green': 5,
    'blue': 6,
    'violet': 7,
    'gray': 8,
    'white': 9,
    'gold': -1,  # For tolerance
    'silver': -2  # For tolerance
}

# Tolerance values
TOLERANCE_VALUES = {
    -1: '±5%',
    -2: '±10%',
}

# Color ranges for OpenCV in HSV (adjust these ranges as needed for accuracy)
COLOR_RANGES = {
    'black': [(0, 0, 0), (180, 255, 50)],
    'brown': [(10, 100, 20), (20, 255, 200)],
    'red': [(0, 150, 50), (10, 255, 255)],
    'orange': [(10, 200, 200), (25, 255, 255)],
    'yellow': [(25, 200, 200), (35, 255, 255)],
    'green': [(35, 100, 100), (85, 255, 255)],
    'blue': [(85, 150, 50), (125, 255, 255)],
    'violet': [(125, 50, 100), (145, 255, 255)],
    'gray': [(0, 0, 50), (180, 50, 200)],
    'white': [(0, 0, 200), (180, 30, 255)],
    'gold': [(20, 150, 100), (30, 200, 200)],
    'silver': [(0, 0, 150), (180, 20, 200)],
}

def identify_color(hsv_pixel):
    """Identify the color based on HSV pixel values."""
    for color, (lower, upper) in COLOR_RANGES.items():
        if all(lower[i] <= hsv_pixel[i] <= upper[i] for i in range(3)):
            return color
    return None

def decode_resistor(colors):
    """Decode resistor value based on detected colors."""
    if len(colors) == 4:  # 4-band resistor
        value = (COLOR_CODES[colors[0]] * 10 + COLOR_CODES[colors[1]]) * (10 ** COLOR_CODES[colors[2]])
        tolerance = TOLERANCE_VALUES[COLOR_CODES[colors[3]]]
        return f"{value} Ω {tolerance}"
    elif len(colors) == 5:  # 5-band resistor
        value = (COLOR_CODES[colors[0]] * 100 + COLOR_CODES[colors[1]] * 10 + COLOR_CODES[colors[2]]) * (10 ** COLOR_CODES[colors[3]])
        tolerance = TOLERANCE_VALUES[COLOR_CODES[colors[4]]]
        return f"{value} Ω {tolerance}"
    elif len(colors) == 6:  # 6-band resistor
        value = (COLOR_CODES[colors[0]] * 100 + COLOR_CODES[colors[1]] * 10 + COLOR_CODES[colors[2]]) * (10 ** COLOR_CODES[colors[3]])
        tolerance = TOLERANCE_VALUES[COLOR_CODES[colors[4]]]
        temp_coeff = f"{COLOR_CODES[colors[5]]} ppm/°C"
        return f"{value} Ω {tolerance}, {temp_coeff}"
    return "Invalid Resistor"

def process_frame(frame):
    """Process the frame to detect and identify resistor bands."""
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # Preprocessing for better detection
    blurred = cv2.GaussianBlur(hsv_frame, (15, 15), 0)
    mask = cv2.inRange(blurred, np.array([0, 0, 0]), np.array([180, 255, 255]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected_colors = []
    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter small areas
            x, y, w, h = cv2.boundingRect(contour)
            roi = hsv_frame[y:y + h, x:x + w]
            avg_color = np.mean(roi, axis=(0, 1)).astype(int)
            color = identify_color(avg_color)
            if color:
                detected_colors.append(color)

    if detected_colors:
        return decode_resistor(detected_colors)
    return "No Resistor Detected"

def main():
    """Main function to run the resistor decoder."""
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        result = process_frame(frame)
        cv2.putText(frame, result, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Resistor Value Decoder", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
