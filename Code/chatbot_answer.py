import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton
import subprocess
from deep_translator import GoogleTranslator
from gtts import gTTS
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pygame

app = QApplication([])

df = pd.read_csv('alzheimers_chatbot_data.csv')

def preprocess_text(text):
    return text.lower()

df['Preprocessed_Question'] = df['Question'].apply(preprocess_text)
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Preprocessed_Question'])

def get_best_answer(user_query):
    query_vector = vectorizer.transform([preprocess_text(user_query)])
    cosine_similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
    best_match_index = cosine_similarities.argmax()
    return df.iloc[best_match_index]['Answer'], cosine_similarities[best_match_index]

def speak(text, lang='en'):
    audio_file = 'output.mp3'
    gTTS(text=text, lang=lang).save(audio_file)
    return audio_file

def voice():
    with open("lang.txt") as file:
        target_lang = file.read()
    with open("answer.txt") as file:
        translated_answer = GoogleTranslator(source='en', target=target_lang).translate(file.readlines()[1])
    pygame.mixer.init()
    pygame.mixer.Sound(speak(translated_answer, lang=target_lang)).play()
    pygame.time.delay(int(pygame.mixer.Sound('output.mp3').get_length() * 1000))
    pygame.mixer.quit()

def answer_button():
    answer, _ = get_best_answer(input_box.text())
    with open('answer.txt', "w") as file:
        file.write(f"{input_box.text()}\n{answer}")
    window.close()
    subprocess.run(["python", "chatbot_answer.py"])

def lang_change():
    subprocess.run(["python", "change_lang.py"])

def wrap_text(text, width=100):
    words = text.split()
    lines, current_line = [], ""
    for word in words:
        if len(current_line) + len(word) + 1 > width:
            lines.append(current_line)
            current_line = word
        else:
            current_line += (" " + word) if current_line else word
    if current_line:
        lines.append(current_line)
    return "\n".join(lines)

window = QWidget()
window.setWindowTitle("Chatbot")
window.setGeometry(0, 0, 1200, 650)
window.paintEvent = lambda event: QPainter(window).drawPixmap(0, 0, window.width(), window.height(), QPixmap('background.jpg'))

with open("answer.txt", "r") as file:
    lines = [line.strip() for line in file]

text_label = QLabel(wrap_text(lines[0]), window)
text_label.setGeometry(100, 100, window.width()-200, 150)
text_label.setAlignment(Qt.AlignLeft)
text_label.setStyleSheet("color: white; font-size: 18px; font-family: Times-of-roman;font-weight:bold")

text_label = QLabel(wrap_text(lines[1]), window)
text_label.setGeometry(100, 150, window.width()-200, 150)
text_label.setAlignment(Qt.AlignLeft)
text_label.setStyleSheet("color: yellow; font-size: 18px; font-family: Times-of-roman; font-weight: bold;")

input_box = QLineEdit(window)
input_box.setGeometry(10, window.height() - 50, window.width() - 200, 40)

button_voice = QPushButton("Voice", window)
button_voice.setGeometry(10, window.height() - 90, 80, 30)
button_voice.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial; font-weight: bold;")
button_voice.clicked.connect(voice)

button_ans = QPushButton("Answer", window)
button_ans.setGeometry(window.width() - 150, window.height() - 50, 100, 40)
button_ans.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial; font-weight: bold;")
button_ans.clicked.connect(answer_button)

button_lang = QPushButton("Language Change", window)
button_lang.setGeometry(100, window.height() - 90, 150, 30)
button_lang.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial; font-weight: bold;")
button_lang.clicked.connect(lang_change)

def predict():
    subprocess.run(["python", "prediction.py"])

button_prediction = QPushButton("Predict The Alzheimer", window)
button_prediction.setGeometry(260, window.height() - 90, 170, 30)
button_prediction.setStyleSheet("background-color: black; color: red; font-size: 15px; font-family: Arial; font-weight: bold;")
button_prediction.clicked.connect(predict)

window.show()
sys.exit(app.exec_())
