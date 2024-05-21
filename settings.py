import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCE_DIR = f'{ROOT_DIR}/resources'

MUSIC = f"{RESOURCE_DIR}/music_files/"
FILES_UI = f"{RESOURCE_DIR}/ui_files/"
IMAGE = f"{RESOURCE_DIR}/image_files/"
FONTS_DIR = f"{RESOURCE_DIR}/font_files/"

FONT_AWESOME = f'{FONTS_DIR}/Font Awesome 6 Free-Solid-900.otf'

DB_FILE = f"{ROOT_DIR}/app_data.db"

PLAYLISTS = {
    'sad': {
        MUSIC + "voila.mp3":        IMAGE + "sad.jpg",
        MUSIC + "sad_snow.mp3":     IMAGE + "sad.jpg",
        MUSIC + "sad_pretend.mp3":  IMAGE + "sad.jpg"
    },
    'neutral': {
        MUSIC+"aach.mp3":       IMAGE+ "neu.jpg",
        MUSIC+"neu_sen.mp3":    IMAGE+ "neu.jpg",
        MUSIC+"neu_shopen.mp3": IMAGE+ "neu.jpg"
    },
    'happy': {
        MUSIC+"happy_love.mp3": IMAGE+"happy.jpg",
        MUSIC+"sedaja.mp3":     IMAGE+"happy.jpg",
        MUSIC+"happy_ball.mp3": IMAGE+ "happy.jpg"
    }
}

USER_INFO = {
    'username': ''
}

WIDGETS = {}