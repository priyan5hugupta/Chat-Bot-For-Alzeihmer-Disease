from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QLabel
from inference_sdk import InferenceHTTPClient

app = QApplication([])

def wrap_text(text, width=10):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(current_line)
            current_line = word
        else:
            current_line += (" " + word) if current_line else word
    if current_line: lines.append(current_line)
    return "\n".join(lines)

def preprocess_image():
    with open("address.txt", "r") as file:
        path = file.read()
    CLIENT = InferenceHTTPClient(api_url="https://detect.roboflow.com", api_key="QAVrvE2bcvfwIMMn2DMU")
    result = CLIENT.infer(path, model_id="alzeihmer-fv3mu/1")
    text_label1.setText(f"Prediction : {result['predicted_classes'][0]}")

def browse_file():
    file_path, _ = QFileDialog.getOpenFileName(window, "Select File", "", "All Files (*)")
    if file_path:
        text_label.setText(f"Selected File : {wrap_text(file_path, width=18)}")
        with open("address.txt", "w") as file:
            file.write(file_path)

window = QMainWindow()
window.setWindowTitle("Select Language")
window.setGeometry(550, 100, 500, 450)
window.paintEvent = lambda event: QPainter(window).drawPixmap(0, 0, window.width(), window.height(), QPixmap('background.jpg'))

button = QPushButton("Browse", window)
button.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial;font-weight: bold;")
button.setGeometry(200, 50, 100, 40)

text_label = QLabel("", window)
text_label.setGeometry(100, 100, 300, 150)
text_label.setAlignment(Qt.AlignLeft)
text_label.setStyleSheet("color: white; font-size: 15px; font-family: Arial;")

text_label1 = QLabel("", window)
text_label1.setGeometry(100, 300, 300, 150)
text_label1.setAlignment(Qt.AlignLeft)
text_label1.setStyleSheet("color: white; font-size: 15px; font-family: Arial;")

analyze_button = QPushButton("Diagnosis", window)
analyze_button.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial;font-weight: bold;")
analyze_button.setGeometry(200, 250, 100, 40)

button.clicked.connect(browse_file)
analyze_button.clicked.connect(preprocess_image)

window.show()
app.exec_()
