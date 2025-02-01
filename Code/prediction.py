from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QPainter
import subprocess

app = QApplication([])

def run_script(script):
    subprocess.run(["python", script])

window = QMainWindow()
window.setWindowTitle("Predict The MRI")
window.setGeometry(550, 100, 500, 350)
window.paintEvent = lambda event: QPainter(window).drawPixmap(0, 0, window.width(), window.height(), QPixmap('background.jpg'))

text_label = QLabel("Select Input Image Source", window)
text_label.setGeometry(0, 0, window.width(), 50) 
text_label.setAlignment(Qt.AlignCenter) 
text_label.setStyleSheet("color: white; font-size: 40px; font-family: Arial;")

buttons = [("Camera", 200, 100, "camera.py"), ("Browse", 200, 250, "browse.py")]
for text, x, y, script in buttons:
    btn = QPushButton(text, window)
    btn.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial; font-weight: bold;")
    btn.setGeometry(x, y, 100, 40)
    btn.clicked.connect(lambda checked, script=script: run_script(script))

window.show()
app.exec_()
