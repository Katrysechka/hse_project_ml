import sys, os
import sqlite3
import hashlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QUrl, QSize, QRect
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QSlider, QStyle,
                             QSizePolicy, QHBoxLayout, QLabel, QVBoxLayout,
                             QSplashScreen, QMainWindow, QFrame)
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, QUrl, QDir
from PyQt5.QtGui import QPixmap, QPalette, QColor, QPainter, QBitmap, QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QStackedWidget, QCalendarWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, QScrollArea, QRadioButton

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox, QTabWidget, QWidget
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QUrl, QEasingCurve, QDir
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton
from databases import Database
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtGui import QPixmap
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QTimer, Qt

main_user = None
MUSIC = "./music_files/"
FILES_UI= "./ui_files/"
IMAGE = "./image_files/"


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi(FILES_UI+"LYE.ui", self)
        self.widget = widget
        self.login.clicked.connect(self.login_account)
        self.create.clicked.connect(self.create_account)
        self.about_us.clicked.connect(self.about_us_function)

    # for login connection
    def login_account(self):
        login = LoginScreen()
        self.widget.addWidget(login)
        open_login_widget = self.widget.currentIndex() + 3 
        self.widget.setCurrentIndex(open_login_widget)  
        index = self.widget.indexOf(login)
        print("Login_account", index)

    # for create connection
    def create_account(self):
        create = CreateAccScreen()
        self.widget.addWidget(create)
        open_login_widget = self.widget.currentIndex() + 2  
        self.widget.setCurrentIndex(open_login_widget) 
        index = self.widget.indexOf(create)
        print("Create_account", index)

    # for rating connection
    def about_us_function(self):
        self.rating_window = RatingWindow()
        self.rating_window.show()


class LoginScreen(QDialog):

    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi(FILES_UI+"LYElog.ui", self)
        self.passwordd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.loginn.clicked.connect(self.login_function)
        self.prev.clicked.connect(self.prev_function)

    # back button
    def prev_function(self):
        self.error_message1.clear()
        current_index = widget.currentIndex()
        print("Index_prev", current_index)
        if current_index > 0:
            return_welcome_widget = current_index - 3
            widget.setCurrentIndex(return_welcome_widget)

    def login_function(self):
        user = self.name.text()
        password = self.passwordd.text()

        if len(user) == 0 or len(password) == 0:
            self.error_message1.setText("Not all fields are filled in.")
            return

        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            data = 'SELECT password FROM login_info WHERE username =\'' + user + "\'"
            cur.execute(data)
            result_pass = cur.fetchone()

            if result_pass != None and result_pass[0] == password:
                print("Successfully logged in.")
                global main_user
                main_user = user
                current_index = widget.currentIndex()
                open_main_window = current_index - 2
                if current_index > 0:
                    widget.setCurrentIndex(open_main_window)
            else:
                self.error_message1.setText("Invalid filling")


class CreateAccScreen(QMainWindow):

    def __init__(self):
        super(CreateAccScreen, self).__init__()
        loadUi(FILES_UI+"LYEcreate.ui", self)

        self.passwordd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passwordd_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.signupfunction)
        self.prev.clicked.connect(self.prevfunction)

    # back button
    def prevfunction(self):
        self.error_message.clear()
        current_index = widget.currentIndex()
        if current_index > 0:
            widget.setCurrentIndex(current_index - 2)

    def signupfunction(self):
        user = self.name.text()
        password = self.passwordd.text()
        confirmpassword = self.passwordd_2.text()

        if len(user) == 0 or len(password) == 0 or len(confirmpassword) == 0:
            self.error_message.setText("Not all fields are filled in.")

        elif password != confirmpassword:
            self.error_message.setText("Passwords mismatch.")
        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            user_info = [user, password]
            print(3)
            cur.execute('INSERT INTO login_info (username, password) VALUES (?,?)', user_info)
            print("Successfully logged in.")
            self.error_message.setText("Creation is comlete. Go to LOGIN.")
            conn.commit()
            conn.close()

class RatingWindow(QDialog):
    def __init__(self):
        super(RatingWindow, self).__init__()
        self.setGeometry(350, 273, 400, 200)
        self.setWindowTitle("Info")
        layout = QVBoxLayout()

        hello_label = QLabel("Listen Your Emotion:", self)
        hello_label.setAlignment(QtCore.Qt.AlignCenter)
        hello_label.setStyleSheet("font-size: 20px; font-family: 'Snell Roundhand'; font-weight: bold;")
        hello_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
        layout.addWidget(hello_label)
        self.setWindowModality(Qt.ApplicationModal)
        content_widget = QWidget()
        
        self.about_text_label = QLabel("")
        self.about_text_label.setWordWrap(True) 
        
        # adding buttons
        about_us_button = QPushButton("О нас")
        chat_support_button = QPushButton("Чат с поддержкой")
        rate_app_button = QPushButton("Оцените приложение")

        about_us_button.setAutoDefault(False) 
        chat_support_button.setAutoDefault(False)  
        rate_app_button.setAutoDefault(False) 

        # click-connect 
        about_us_button.clicked.connect(self.show_about_us_text)
        chat_support_button.clicked.connect(self.show_chat_support_text)
        rate_app_button.clicked.connect(self.show_rate_app_text)
        
        # adding widgets into layout
        layout.addWidget(about_us_button)
        layout.addWidget(chat_support_button)
        layout.addWidget(rate_app_button)
        layout.addWidget(self.about_text_label)
        self.setLayout(layout)

        about_us_button.clicked.connect(lambda: self.set_button_color(about_us_button))
        chat_support_button.clicked.connect(lambda: self.set_button_color(chat_support_button))
        rate_app_button.clicked.connect(lambda: self.set_button_color(rate_app_button))
        self.current_button = None

    def set_button_color(self, button):
        if self.current_button:
            self.current_button.setStyleSheet("")
            self.current_button.setStyleSheet("color: black;")
        button.setStyleSheet("background-color: #778899; color: white;")
        # update button
        self.current_button = button
        
    def resizeEvent(self, event):
        if self.size().height() == 500:
            self.setGeometry(350, 273, 400, 500)  
        elif self.size().height() == 100:
            self.setGeometry(350, 273, 400, 100) 
        elif self.size().height() == 300:
            self.setGeometry(350, 273, 400, 300)       
        event.accept()
        
    def show_about_us_text(self):
        self.setGeometry(350, 273, 400, 500)
        about_us_text = (
            "\"Listen Your Emotion\" - это удивительное приложение, способное чувствовать и отражать ваше настроение через музыку. "
            "Оно сканирует ваше лицо, захватывая каждое выражение и эмоцию, чтобы подобрать идеальный трек, который соответствует вашему текущему состоянию души.\n\n"
            "С помощью \"Listen Your Emotion\" вы можете погрузиться в мир музыки, созданной специально для вас. От меланхоличных мелодий до бодрящих ритмов - приложение подберет идеальный саундтрек для каждого вашего настроения.\n\n"
            "Позвольте себе окунуться в атмосферу гармонии и эмоций с \"Listen Your Emotion\" - приложением, которое делает вашу жизнь звучащей и красивой."
        )
        self.about_text_label.setText(about_us_text)
        
    def show_chat_support_text(self):
        self.setGeometry(350, 273, 400, 100) 
        self.about_text_label.setText("<a href='https://t.me/DatbyDay_bot'>Связаться с нами в Telegram</a>")
        self.about_text_label.setOpenExternalLinks(True) 
        
    def show_rate_app_text(self):
        self.setGeometry(350, 273, 400, 300) 
        rate_app_text = "Пожалуйста, оцените наше приложение. Ваш отзыв очень важен для нас и поможет нам сделать его еще лучше!"
        self.about_text_label.setText(rate_app_text)


def emotion_to_number(emotion):
    if emotion.lower() in ['angry', 'disgust', 'fear', 'sad']:
        return 1
    elif emotion.lower() == 'neutral':
        return 2
    else:
        return 3


def choose_playlist(number_):  # for connection with other members

    global choose_em_playlist

    if number_ == 1:
        choose_em_playlist = {
            MUSIC+"voila.mp3":IMAGE+ "sad.jpg",
            MUSIC+"sad_snow.mp3": IMAGE+"sad.jpg",
            MUSIC+"sad_pretend.mp3":IMAGE+ "sad.jpg"
        }
    elif number_ == 2:
        choose_em_playlist = {
            MUSIC+"happy_love.mp3": IMAGE+"happy.jpg",
            MUSIC+"sedaja.mp3": IMAGE+"happy.jpg",
            MUSIC+"happy_ball.mp3":IMAGE+ "happy.jpg"
        }
    elif number_ == 3:
        choose_em_playlist = {
            MUSIC+"aach.mp3": IMAGE+"neu.jpg",
            MUSIC+"neu_sen.mp3":IMAGE+ "neu.jpg",
            MUSIC+"neu_shopen.mp3":IMAGE+ "neu.jpg"
        }


# emotion addition
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
                "font-family: 'Snell Roundhand', cursive; font-size: 25px; font-stretch: normal; color: #222222;")
        else:
            self.label.setStyleSheet(
                "font-family: 'Snell Roundhand', cursive; font-size: 25px; font-stretch: normal; color: #FFFFFF;")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.tracks = {
            MUSIC+"aach.mp3": IMAGE+"neu.jpg",
            MUSIC+"sedaja.mp3": IMAGE+"happy.jpg",
            MUSIC+"voila.mp3": IMAGE+"sad.jpg"
        }

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('LYE')

        self.current_index = 0  # for songs
        self.current_playlist = 3  # neutral - basic
        self.playlist_index = {}

        # color theme for now
        self.light_theme = True

        # button to save your favorite tracks
        self.heart_button = QPushButton("❤")
        self.heart_button.setFixedSize(30, 30)
        self.heart_button.setToolTip("Add to favorites")
        self.heart_button.setStyleSheet("background-color: #BA55D3; border-radius: 5px;")
        self.heart_button.clicked.connect(self.show_message)

        self.center_screen()

        # side buttons

        # self.create_tag("LYE")
        # pixmap = QPixmap(IMAGE+"profileA-2.jpg")
        # icon = QIcon(pixmap)

        # self.your_lye_button = QPushButton(self)
        # self.your_lye_button.setStyleSheet("""
        #     QPushButton {
        #         border-radius: 50px;
        #         padding: 0px;
        #         color: white;
        #     }
        # """)

        # self.your_lye_button.setIcon(icon)
        # self.your_lye_button.setIconSize(QSize(50, 50))
        # self.your_lye_button.clicked.connect(self.open_new_window)
        # self.your_lye_button.move(15, 20)

        self.your_lye_button = QPushButton("Your LYE", self)
        self.your_lye_button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                padding: 10px 20px;
                color: white;
                background-color: #AAAAAA; 
            }
        """)
        self.your_lye_button.clicked.connect(self.open_new_window)

    
        self.initUI()
        
        self.set_theme(self.light_theme)
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
        button.setGeometry(10, 10, button_size + 20, button_size)
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

    def open_new_window(self):
        print('sjhfgwjfrfjfberfgerf')
        self.new_window = Profile()
        self.new_window.show()


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

        default_image = IMAGE+"aaa.jpg"
        pixmap = QPixmap(default_image)
        pixmap = pixmap.scaled(500, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()

        # buttons
        btn5 = QPushButton('Next', clicked=self.next_m)
        btn6 = QPushButton('Prev', clicked=self.prev_m)
        btn4 = QPushButton(clicked=self.volume_st)
        btn4.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        btn1 = QPushButton(clicked=self.open_file)
        btn1.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # slider
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(20)
        self.volume_slider.valueChanged.connect(self.change_volume)
        volume_layout = QHBoxLayout()
        volume_layout.addWidget(self.volume_slider)

        # play
        self.btn_play = QPushButton()
        self.btn_play.setEnabled(False)
        self.btn_play.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

        # label
        self.label = QLabel()
        self.layout.addLayout(musicControl)
        self.layout.addLayout(volumeControl)
        self.layout.addLayout(button_layout)

        # add buttons
        button_layout.addWidget(btn6)
        button_layout.addWidget(btn4)
        button_layout.addWidget(btn1)
        button_layout.addWidget(btn5)
        button_layout.addWidget(self.volume_slider)
        button_layout.addWidget(self.heart_button)

        # Desired order for arrangement

        button_layout.setStretch(0, 1)
        button_layout.setStretch(1, 1)
        button_layout.setStretch(2, 1)
        button_layout.setStretch(3, 1)
        button_layout.setStretch(4, 4)
        button_layout.setStretch(5, 1)

        # emotional buttons

        self.emotion_panel = EmotionPanel()  # Define emotion_panel as an instance attribute
        self.layout.addWidget(self.emotion_panel)

        # for low panel

        button_area.setFixedSize(770, 70)
        self.layout.addWidget(button_area)

        # connect emotional

        self.emotion_panel.btn_sad.clicked.connect(self.sad_playlist)
        self.emotion_panel.btn_neutral.clicked.connect(self.happy_playlist)
        self.emotion_panel.btn_happy.clicked.connect(self.neutral_playlist)

        self.player = QMediaPlayer()
        self.player.mediaStatusChanged.connect(self.on_media_status_changed)


    def set_theme(self, light_theme):
        self.light_theme = light_theme
        color_hex = "#AAAAAA" if self.light_theme else "#FFFFFF"
        color = QColor(color_hex)
        c = self.palette()
        c.setColor(QPalette.Window, color)
        self.setPalette(c)
        self.emotion_panel.update_theme(self.light_theme)

        # sun icon
        self.theme_button = QPushButton(self)
        self.theme_button.setIcon(QIcon(IMAGE+"sun.jpg"))
        self.theme_button.setIconSize(QSize(30, 30))
        self.theme_button.clicked.connect(self.change_theme)
        self.theme_button.setGeometry(QRect(self.width() - 40, 10, 30, 30))
        self.theme_button.move(self.width() - 40, 10)
        self.theme_button.setStyleSheet("border-radius: 15px;")

    def change_theme(self):
        self.set_theme(not self.light_theme)

    def show_message(self):
        QMessageBox.about(self, "Message", "Added to favorites ❤ ")

    def set_playlist(self, playlist):  # for connection words and numbers
        if playlist == 1:
            choose_playlist(1)
            self.current_playlist = 1
            self.tracks = choose_em_playlist
        elif playlist == 2:
            choose_playlist(2)
            self.current_playlist = 2
            self.tracks = choose_em_playlist
        elif playlist == 3:
            choose_playlist(3)
            self.current_playlist = 3
            self.tracks = choose_em_playlist
        self.current_index = self.playlist_index.get(self.current_playlist,
                                                     0)  # index of the current track in this playlist
        self.open_file()

    def sad_playlist(self):
        self.set_playlist(1)

    def neutral_playlist(self):
        self.set_playlist(2)

    def happy_playlist(self):
        self.set_playlist(3)

    def change_volume(self, value):
        self.player.setVolume(value)

    def initTracks(self):

        choose_playlist(self.current_playlist)
        self.playlist_index = {1: 0, 2: 0, 3: 0}
        self.tracks = choose_em_playlist

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
        self.playlist_index[self.current_playlist] = self.current_index
        self.open_file()

    def on_media_status_changed(self, state):  # auto transition to next track
        if state == QMediaPlayer.EndOfMedia:
            self.next_m()

    def prev_m(self):
        self.current_index = (self.current_index - 1) % len(self.tracks)
        self.playlist_index[self.current_playlist] = self.current_index
        self.open_file()

    def update_image(self):
        current_track = list(self.tracks.keys())[self.current_index]
        image_filename = self.tracks[current_track]
        if image_filename:
            image_path = os.path.join(os.getcwd(), image_filename)
        else:
            image_path = IMAGE+"lye.jpg"
        pixmap = QPixmap(image_path)
        pixmap = pixmap.scaled(600, 500, Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)
        self.image_label.adjustSize()

    def show_splash(self):
        pixmap = QPixmap(IMAGE+"LYEE.jpg")
        pixmap = pixmap.scaled(791, 600)
        splash = QSplashScreen(pixmap)
        splash.setFixedSize(pixmap.size())
        splash.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        splash.move(splash.pos().x(), splash.pos().y() )
        splash.show()

        # add animation for splash-screen

        animation = QPropertyAnimation(splash, b"windowOpacity")
        animation.setDuration(3000)
        animation.setStartValue(0.96)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.OutCubic)
        animation.start()

        QTimer.singleShot(1500, splash.close)
        splash.show()
        return splash

class Profile(QDialog):
    def __init__(self):
        super(Profile, self).__init__()
        self.setGeometry(350, 273, 400, 100)
        self.setWindowTitle("Profile")
        layout = QVBoxLayout()

        hello_label = QLabel("Listen Your Emotion:", self)
        hello_label.setAlignment(QtCore.Qt.AlignCenter)
        hello_label.setStyleSheet("font-size: 20px; font-family: 'Snell Roundhand'; font-weight: bold;")
        hello_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
        layout.addWidget(hello_label)
        self.setWindowModality(Qt.ApplicationModal)
        content_widget = QWidget()
        
        self.about_text_label = QLabel("")
        self.about_text_label.setWordWrap(True) 
        
        # adding buttons
        profile_button = QPushButton("Показать профиль")
        add_profile_button = QPushButton("Добавить информацию")

        profile_button.setAutoDefault(False) 
        add_profile_button.setAutoDefault(False)  

        # click-connect 
        profile_button.clicked.connect(self.show_profile_text)
        add_profile_button.clicked.connect(self.show_add_profile_text)
        
        # adding widgets into layout
        layout.addWidget(profile_button)
        layout.addWidget(add_profile_button)
        layout.addWidget(self.about_text_label)
        self.setLayout(layout)

        profile_button.clicked.connect(lambda: self.set_button_color(profile_button))
        add_profile_button.clicked.connect(lambda: self.set_button_color(add_profile_button))
        self.current_button = None

    def set_button_color(self, button):
        if self.current_button:
            self.current_button.setStyleSheet("")
            self.current_button.setStyleSheet("color: black;")
        button.setStyleSheet("background-color: #778899; color: white;")
        # update button
        self.current_button = button
        
    def resizeEvent(self, event):
        if self.size().height() == 500:
            self.setGeometry(350, 273, 400, 500)  
        elif self.size().height() == 100:
            self.setGeometry(350, 273, 400, 100) 
        elif self.size().height() == 300:
            self.setGeometry(350, 273, 400, 300)       
        event.accept()
        
    def show_profile_text(self):
        self.setGeometry(350, 273, 400, 500)
        self.new_window = Profile1()
        self.new_window.show()
        
    def show_add_profile_text(self):
        self.setGeometry(350, 273, 400, 100) 
        self.new_window = Profile2()
        self.new_window.show()

# profile LYE
class Profile2(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Profile")
        self.setWindowModality(Qt.ApplicationModal)
        self.resize(791, 300)

        # profile information
        self.name_edit = QLineEdit(self)
        self.name_edit.setPlaceholderText("Name")
        self.surname_edit = QLineEdit(self)
        self.surname_edit.setPlaceholderText("Surname")

        # hb
        self.calendar = QCalendarWidget(self)

        # profile adding
        self.artist_edit = QLineEdit(self)
        self.artist_edit.setPlaceholderText("Favorite performer")
        self.song_edit = QLineEdit(self)
        self.song_edit.setPlaceholderText("Favorite song")
        self.genre_edit = QLineEdit(self)
        self.genre_edit.setPlaceholderText("Favorite genre")

        # Sex choose
        self.gender_label = QLabel("Sex:", self)
        self.female_radio = QRadioButton("female", self)
        self.male_radio = QRadioButton("male", self)
        self.gender_group = QHBoxLayout()
        self.gender_group.addWidget(self.female_radio)
        self.gender_group.addWidget(self.male_radio)

        # Save changes
        self.save_button = QPushButton("Save", self)
        self.save_button.clicked.connect(self.save_profile)

        # vertical layout
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Name:", self))
        layout.addWidget(self.name_edit)
        layout.addWidget(QLabel("Surname:", self))
        layout.addWidget(self.surname_edit)
        layout.addWidget(QLabel("HB:", self))
        layout.addWidget(self.calendar)
        layout.addWidget(QLabel("Singer:", self))
        layout.addWidget(self.artist_edit)
        layout.addWidget(QLabel("Song:", self))
        layout.addWidget(self.song_edit)
        layout.addWidget(QLabel("Genre:", self))
        layout.addWidget(self.genre_edit)
        layout.addWidget(self.gender_label)
        layout.addLayout(self.gender_group)
        layout.addWidget(self.save_button)

        # connection
        self.conn = sqlite3.connect("show_data.db")
        self.cur = self.conn.cursor()
        self.load_profile()

    def load_profile(self):
        self.cur.execute("SELECT * FROM login_info")
        user_data = self.cur.fetchone()

        if user_data:
            self.name_edit.setText(user_data[1])
            self.surname_edit.setText(user_data[2])
            self.calendar.setSelectedDate(user_data[3])
            self.artist_edit.setText(user_data[4])
            self.song_edit.setText(user_data[5])
            self.genre_edit.setText(user_data[6])
            gender = user_data[7]
            if gender == 0:
                self.female_radio.setChecked(True)
            elif gender == 1:
                self.male_radio.setChecked(True)

    def save_profile(self):
        name = self.name_edit.text()
        surname = self.surname_edit.text()
        birthday = self.calendar.selectedDate().toString("yyyy-MM-dd")
        favorite_artist = self.artist_edit.text()
        favorite_song = self.song_edit.text()
        favorite_genre = self.genre_edit.text()

        gender = 0 if self.female_radio.isChecked() else 1

    # id from another table
        self.cur.execute("SELECT username FROM login_info LIMIT 1")
        id = self.cur.fetchone()[0]

    # add changes
        self.cur.execute("INSERT INTO profile (id, name, surname, birthday, favorite_artist, favorite_song, favorite_genre, gender) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (id, name, surname, birthday, favorite_artist, favorite_song, favorite_genre, gender))
        self.conn.commit()
        QMessageBox.information(self, "Сохранено", "Данные профиля сохранены в базе данных")


# add_profile LYE
class Profile1(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        uic.loadUi(FILES_UI+'addprofile.ui', self)
        self.save_ch.clicked.connect(self.save_chh())
        self.prevv.clicked.connect(self.prevfunction())
        self.user_namename.setText(main_user)

    def prevfunction(self):
        self.error_message1.clear()
        current_index = widget.currentIndex()
        if current_index > 0:
            widget.setCurrentIndex(current_index - 2)

    def save_chh(self):
        user1 = self.firstname.text()
        user2 = self.lastname.text()

        if len(user1) == 0 or len(user2) == 0:
            self.label_2.setText("Not all fields are filled in.")

        else:
            conn = sqlite3.connect("shop_data.db")
            cur = conn.cursor()
            user_info = [user1, user2]
            cur.execute('INSERT INTO login_info_app (first_name, last_name) VALUES (?,?)', user_info)
            print("Successfully save changes.")
            conn.commit()
            conn.close()
            current_index = widget.currentIndex()
            if current_index > 0:
                widget.setCurrentIndex(current_index - 2)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    widget = QStackedWidget()
    welcome = WelcomeScreen()
    widget.addWidget(welcome)

    mainWindow = MainWindow()
    widget.addWidget(mainWindow)
    widget.setFixedWidth(791)
    widget.setFixedHeight(600)
    widget.setWindowFlags(Qt.WindowStaysOnTopHint)
    widget.move(widget.pos().x()+335, widget.pos().y()+180)
    widget.show()

    splash = mainWindow.show_splash()
    splash.show()

    QTimer.singleShot(1500, lambda: widget.setCurrentIndex(-1))
    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
