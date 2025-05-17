import sqlite3
import utils.file_loader as file_loader

class SQL:
    def __init__(self):
        try:
            self.__db_connection = sqlite3.connect(file_loader.load_dotenv()["DATABASE_LOCATION"])
        except sqlite3.Error as e:
            print(e)

    def __del__(self):
        try:
            self.__db_connection.commit()
        except sqlite3.Error as e:
            print(e)
        self.__db_connection.close()

    def execute(self, sql):
        try:
            self.__db_connection.execute(sql)
        except sqlite3.Error as e:
            print(e)
        del self

    def fetchone(self, sql):
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchone()
        except sqlite3.Error as e:
            result = None
            print(e)

        del self
        return result
    
    def fetchall(self, sql):
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute(sql)
            result = cursor.fetchall()
        except sqlite3.Error as e:
            result = None
            print(e)

        del self
        return result
    
    def setup(self):
        self.execute("CREATE TABLE IF NOT EXISTS users (discord_id INTEGER PRIMARY KEY, ingame_name TEXT NOT NULL UNIQUE, mmr INTEGER NOT NULL DEFAULT 0); ")
        
