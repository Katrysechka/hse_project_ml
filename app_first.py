import sys, os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QSlider, QStyle,
                             QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout,
                             QSplashScreen, QMainWindow)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QUrl, QDir
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter, QBitmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.tracks = {
            "aach.mp3": "lakeu.jpg",
            "sedaja.mp3": "sed.jpg",
            "voila.mp3": "voilaa.jpg"
        }
        self.current_index = 0

        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('LYE')

        # color theme
        color_hex = "#DCDCDC"
        color = QColor(color_hex)
        c = self.palette()
        c.setColor(QPalette.Window, color)
        self.setPalette(c)
        self.center_screen()
        self.create_tag("LYE")
        self.initUI()
        self.show()

    # central location
    def center_screen(self):
        app_geometry = QApplication.desktop().availableGeometry()
        wind_geometry = self.frameGeometry()
        wind_geometry.moveCenter(app_geometry.center())
        self.move(wind_geometry.topLeft())

    # tag
    def create_tag(self, text):
        button = QPushButton(text, self)
        button_size = 45
        button.setGeometry(10, 10, button_size, button_size)
        button.setStyleSheet(
            "QPushButton {"
            "    background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #AAAAAA);"
            "    border: none;"
            "    font-weight: bold;"
            "    text-shadow: 2px 2px 2px rgba(0, 0, 0, 0.5);"
            "    color: #222222;"
            f"    border-radius: {button_size // 2}px;"
            "}"
        )

    def initUI(self):
        self.initTracks()

        self.player = QMediaPlayer()
        self.layout = QVBoxLayout()

        self.setLayout(self.layout)
        button_area = QWidget()
        button_layout = QHBoxLayout(button_area)
        button_area.setStyleSheet("background-color: white; border-radius: 10px;")
        button_area.setFixedHeight(50)
        volumeControl = QHBoxLayout()
        musicControl = QHBoxLayout()

        # images

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.image_label)

        # buttons

        btn5 = QPushButton('Next', clicked=self.next_m)
        btn6 = QPushButton('Prev', clicked=self.prev_m)
        btn4 = QPushButton(clicked=self.volume_st)
        btn4.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        btn1 = QPushButton(clicked=self.open_file)
        btn1.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # play
        self.btn_play = QPushButton()
        self.btn_play.setEnabled(False)
        self.btn_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(5)
        self.volume_slider.valueChanged.connect(self.change_volume)
        musicControl.addWidget(self.volume_slider)

        # label
        self.label = QLabel()
        self.layout.addLayout(musicControl)
        self.layout.addLayout(volumeControl)

        # add buttons
        button_layout.addWidget(btn6)
        button_layout.addWidget(btn4)
        button_layout.addWidget(btn1)
        button_layout.addWidget(btn5)

        button_area.setFixedSize(550, 50)
        self.layout.addWidget(button_area)

    def change_volume(self, value):
        self.player.setVolume(value)

    def initTracks(self):
        self.tracks = {
            "aach.mp3": "lakeu.jpg",
            "sedaja.mp3": "sed.jpg",
            "voila.mp3": "voilaa.jpg"
        }
        self.current_index = 0

    def volume_pl(self):
        curr = self.player.volume()
        self.player.setVolume(curr + 20)

    def volume_ms(self):
        curr = self.player.volume()
        self.player.setVolume(curr - 20)

    def volume_st(self):
        self.player.setMuted(not self.player.isMuted())

    def open_file(self):
        current_track = list(self.tracks.keys())[self.current_index]
        track_path = os.path.join(os.getcwd(), current_track)
        media = QMediaContent(QUrl.fromLocalFile(track_path))

        self.player.stop()
        self.player.setMedia(media)
        self.player.play()
        self.update_image()

    def next_m(self):
        self.current_index = (1 + self.current_index) % len(self.tracks)
        self.open_file()

    def prev_m(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.open_file()

    def update_image(self):
        current_track = list(self.tracks.keys())[self.current_index]
        image_filename = self.tracks[current_track]
        image_path = os.path.join(os.getcwd(), image_filename)
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()

    def show_splash(self):
        pixmap = QPixmap("LYEE.jpg")
        pixmap = pixmap.scaled(600, 400)

        splash = QSplashScreen(pixmap)
        splash.setFixedSize(pixmap.size())
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.move(splash.pos().x(), splash.pos().y() + 6)
        splash.show()

        # add animation for splash-screen

        animation = QPropertyAnimation(splash, b"windowOpacity")
        animation.setDuration(1500)
        animation.setStartValue(0.96)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()

        QTimer.singleShot(1500, splash.close)
        splash.show()
        return splash


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    splash = ex.show_splash()
    ex.show()
    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Stop music...')
