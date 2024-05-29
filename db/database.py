import sqlite3
from db.models import Profile
from datetime import date
from typing import Optional

from settings import DB_FILE

class Database:
    def __init__(self) -> None:
        self.connection = sqlite3.connect(DB_FILE)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS Profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            birthday DATE,
            fav_artist TEXT,
            fav_song TEXT,
            fav_genre TEXT,
            gender INTEGER
        )
        """)
        self.connection.commit()

    def is_username_taken(self, username: str) -> bool:
        self.cursor.execute("SELECT COUNT(*) as count FROM Profile WHERE username=?", (username,))
        count = self.cursor.fetchone()[0]
        return count > 0

    def get_profile(self, id: int) -> Profile:
        self.cursor.execute("SELECT * FROM Profile WHERE id=?", (id,))
        row = self.cursor.fetchone()
        if row:
            profile = Profile(**dict(row))
            return profile

    def get_profile_by_username(self, username: str) -> Optional[Profile]:
        self.cursor.execute("SELECT * FROM Profile WHERE username=?", (username,))
        row = self.cursor.fetchone()
        if row:
            return Profile(**dict(row))

    def add_profile(self, profile: Profile):
        self.cursor.execute("""
        INSERT INTO Profile (username, password)
        VALUES (?, ?)
        """, (profile.username, profile.password))
        self.connection.commit()

    def edit_profile(self, id: int, profile: Profile):
        self.cursor.execute("""
        UPDATE Profile
        SET username=?, password=?, first_name=?, last_name=?, birthday=?, fav_artist=?, fav_song=?, fav_genre=?, gender=?
        WHERE id=?
        """, (profile.username, profile.password, profile.first_name, profile.last_name, profile.birthday, 
              profile.fav_artist, profile.fav_song, profile.fav_genre, profile.gender, id))
        self.connection.commit()

    def close(self):
        self.connection.close()

database = Database()