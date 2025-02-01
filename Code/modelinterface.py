from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from inference_sdk import InferenceHTTPClient

app = QApplication([])

window = QMainWindow()
window.setWindowTitle("Prediction")
window.setGeometry(550, 100, 300, 100)
window.paintEvent = lambda event: QPainter(window).drawPixmap(0, 0, window.width(), window.height(), QPixmap('background.jpg'))

text_label = QLabel("", window)
text_label.setGeometry(75, 40, 300, 150)
text_label.setAlignment(Qt.AlignLeft)
text_label.setStyleSheet("color: white; font-size: 15px; font-family: Arial;")

CLIENT = InferenceHTTPClient(api_url="https://detect.roboflow.com", api_key="QAVrvE2bcvfwIMMn2DMU")
result = CLIENT.infer("image.jpg", model_id="alzeihmer-fv3mu/1")
text_label.setText(f"Prediction: {result['predicted_classes'][0]}")

window.show()
app.exec_()