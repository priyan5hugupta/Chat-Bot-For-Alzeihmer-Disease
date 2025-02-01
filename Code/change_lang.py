from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

app = QApplication([])

def set_lang(lang):
    with open('lang.txt', "w") as file:
        file.write(lang)
    window.close()

window = QWidget()
window.setWindowTitle("Select Language")
window.setGeometry(550, 200, 320, 100)
window.paintEvent = lambda event: QPainter(window).drawPixmap(0, 0, window.width(), window.height(), QPixmap('background.jpg'))

buttons = [("English", "en", 10, 10), ("Hindi", "hi", 200, 10), ("Spanish", "es", 10, 50), ("French", "fr", 200, 50)]
for text, lang, x, y in buttons:
    btn = QPushButton(text, window)
    btn.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial;font-weight: bold;")
    btn.setGeometry(x, y, 80, 30)
    btn.clicked.connect(lambda checked, lang=lang: set_lang(lang))

window.show()
app.exec_()
