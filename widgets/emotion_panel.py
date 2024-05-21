from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class EmotionPanel(QWidget):
    def __init__(self, light_theme=True):
        super().__init__()
        self.light_theme = light_theme
        self.initUI()

    def initUI(self):
        def_layout = QVBoxLayout()  # for inscription
        emotion_layout = QHBoxLayout()  # for emotion buttons

        # inscription
        self.label = QLabel("Listen your emotion")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if self.light_theme:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 30px; font-stretch: normal; color: #222222;")
        else:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 30px; font-stretch: normal; color: #FFFFFF;")

        def_layout.addWidget(self.label)

        # EMOTION PANEL
        self.btn_sad = QPushButton('Sad')
        self.btn_neutral = QPushButton('Neutral')
        self.btn_happy = QPushButton('Happy')

        emotion_layout.addWidget(self.btn_sad)
        emotion_layout.addWidget(self.btn_neutral)
        emotion_layout.addWidget(self.btn_happy)

        # touch response
        self.btn_sad.clicked.connect(self.set_sad)
        self.btn_neutral.clicked.connect(self.set_neu)
        self.btn_happy.clicked.connect(self.set_happy)

        def_layout.addLayout(emotion_layout)
        self.setLayout(def_layout)

    def reset_colors(self):  # reset prev style
        self.btn_sad.setStyleSheet("")
        self.btn_neutral.setStyleSheet("")
        self.btn_happy.setStyleSheet("")

    def set_sad(self):
        self.reset_colors()
        self.btn_sad.setStyleSheet("background-color: #9370DB;; color: white;")

    def set_neu(self):
        self.reset_colors()
        self.btn_neutral.setStyleSheet("background-color: #87CEEB;; color: white;")

    def set_happy(self):
        self.reset_colors()
        self.btn_happy.setStyleSheet("background-color: #90EE90;; color: white;")

    def update_theme(self, light_theme):
        self.light_theme = light_theme
        if self.light_theme:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 25px; color: #222222;")
        else:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 25px; color: #AD4029;")

