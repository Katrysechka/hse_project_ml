from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class EmotionPanel(QWidget):
    def __init__(self, light_theme=True):
        super().__init__()
        self.light_theme = light_theme
        self.initUI()

    def initUI(self):
        self.def_layout = QVBoxLayout()  # for inscription
        self.genre_layout = QHBoxLayout()  # for genre buttons
        self.emotion_layout = QHBoxLayout()  # for emotion buttons

        # inscription
        self.label = QLabel("Listen your emotion")
        self.label.setAlignment(Qt.AlignCenter)

        if self.light_theme:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 30px; font-stretch: normal; color: #222222;")
        else:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 30px; font-stretch: normal; color: #FFFFFF;")

        self.def_layout.addWidget(self.label)

        # Button to show/hide genre panel
        self.btn_show_genres = QPushButton('Genres')
        self.btn_show_genres.clicked.connect(self.toggle_genres)
        self.def_layout.addWidget(self.btn_show_genres)

        # GENRE PANEL (initially hidden)
        self.btn_classic = QPushButton('Classic')
        self.btn_pop = QPushButton('Pop')
        self.btn_rock = QPushButton('Rock')

        self.genre_layout.addWidget(self.btn_classic)
        self.genre_layout.addWidget(self.btn_pop)
        self.genre_layout.addWidget(self.btn_rock)
        self.genre_widget = QWidget()
        self.genre_widget.setLayout(self.genre_layout)
        self.genre_widget.setVisible(False)  

        self.def_layout.addWidget(self.genre_widget)

        # EMOTION PANEL
        self.btn_sad = QPushButton('Sad')
        self.btn_neutral = QPushButton('Neutral')
        self.btn_happy = QPushButton('Happy')

        self.emotion_layout.addWidget(self.btn_sad)
        self.emotion_layout.addWidget(self.btn_neutral)
        self.emotion_layout.addWidget(self.btn_happy)

        # touch response for genres
        self.btn_classic.clicked.connect(self.set_classic)
        self.btn_pop.clicked.connect(self.set_pop)
        self.btn_rock.clicked.connect(self.set_rock)

        # touch response for emotions
        self.btn_sad.clicked.connect(self.set_sad)
        self.btn_neutral.clicked.connect(self.set_neu)
        self.btn_happy.clicked.connect(self.set_happy)

        self.def_layout.addLayout(self.emotion_layout)  # Add emotion buttons layout and genre buttons
        self.setLayout(self.def_layout)

    def toggle_genres(self):
        is_visible = self.genre_widget.isVisible()
        self.genre_widget.setVisible(not is_visible)

    def reset_colors(self):  # reset prev style
        self.btn_sad.setStyleSheet("")
        self.btn_neutral.setStyleSheet("")
        self.btn_happy.setStyleSheet("")
        self.btn_classic.setStyleSheet("")
        self.btn_pop.setStyleSheet("")
        self.btn_rock.setStyleSheet("")

    def set_sad(self):
        self.reset_colors()
        self.btn_sad.setStyleSheet("background-color: #9370DB;; color: white;")

    def set_neu(self):
        self.reset_colors()
        self.btn_neutral.setStyleSheet("background-color: #87CEEB;; color: white;")

    def set_happy(self):
        self.reset_colors()
        self.btn_happy.setStyleSheet("background-color: #90EE90;; color: white;")

    def set_classic(self):
        self.reset_colors()
        self.btn_classic.setStyleSheet("background-color: #9370DB;; color: white;")

    def set_pop(self):
        self.reset_colors()
        self.btn_pop.setStyleSheet("background-color: #87CEEB;; color: white;")

    def set_rock(self):
        self.reset_colors()
        self.btn_rock.setStyleSheet("background-color: #90EE90;; color: white;")    

    def update_theme(self, light_theme):
        self.light_theme = light_theme
        if self.light_theme:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 25px; color: #222222;")
        else:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 25px; color: #AD4029;")

