import cv2
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton
from PyQt5.QtGui import QImage, QPixmap,QPainter
from PyQt5.QtCore import QTimer
import subprocess

app = QApplication([])

def update_frame():
    ret, frame = cap.read()
    if ret:
        qt_image = QImage(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB).data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
        video_label.setPixmap(QPixmap.fromImage(qt_image))

def capture_image():
    ret, frame = cap.read()
    if ret:
        cv2.imwrite("image.jpg", frame)
        cap.release()
        window.close()
        subprocess.run(["python", "modelinterface.py"])

window = QMainWindow()
window.setWindowTitle("Camera")
window.setGeometry(550, 100, 500, 500)
window.paintEvent = lambda event: QPainter(window).drawPixmap(0, 0, window.width(), window.height(), QPixmap('background.jpg'))

video_label = QLabel(window)
video_label.setGeometry(20, 20, 460, 400)

cap = cv2.VideoCapture(0)

capture_button = QPushButton("Capture Image", window)
capture_button.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial;font-weight: bold;")
capture_button.setGeometry(200, window.height()-70, 110, 40)

timer = QTimer()
timer.start(20)

timer.timeout.connect(update_frame)
capture_button.clicked.connect(capture_image)

window.show()

def close_event():
    cap.release()
    window.close()

app.aboutToQuit.connect(close_event)

app.exec_()
