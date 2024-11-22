# resistor_value_decoder
# Resistor Value Decoder using OpenCV

This project detects and decodes the color bands on resistors in real time using a webcam feed. It identifies resistor values and tolerances based on standard color codes.

---

## 📜 **Features**
- Real-time detection of resistor color bands using OpenCV.
- Decodes 4-band, 5-band, and 6-band resistors.
- Displays decoded resistor value and tolerance on the video feed.

---

## 🛠 **Technologies Used**
- Python
- OpenCV
- NumPy

---

## 🚀 **Setup Instructions**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/resistor-value-decoder.git
   cd resistor-value-decoder
   
Install the required dependencies:
pip install -r requirements.txt

Run the project:
python resistor_decoder.py

📝 How It Works
Captures a live feed from the webcam.
Detects and identifies colors on the resistor using HSV thresholds.
Decodes the resistor value based on standard color codes.
Displays the decoded value and tolerance in real-time.

💡 Future Enhancements
Add support for different resistor formats.
Improve color detection accuracy for varying lighting conditions.
Implement an interactive UI for easier usage.
