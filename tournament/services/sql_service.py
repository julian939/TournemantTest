import logging
import sqlite3

import utils.file_loader as file_loader

class SQLService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        try:
            self.__db_connection = sqlite3.connect(file_loader.load_dotenv()["DATABASE_LOCATION"])
            self.__db_connection.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            self.logger.error(f"DB Connection error: {e}")

    def close(self):
        try:
            self.__db_connection.commit()
            self.__db_connection.close()
        except sqlite3.Error as e:
            self.logger.error(f"DB Close error: {e}")

    def execute(self, sql: str, params: tuple = ()):
        try:
            cursor = self.__db_connection.cursor()
            cursor.execute(sql, params)
            self.__db_connection.commit()
            sql_str = str(sql).strip().upper()
            if sql_str.startswith("INSERT"):
                return cursor.lastrowid
            return None
        except sqlite3.Error as e:
            self.logger.error(f"SQL execute error: {e} -- Query: {sql} -- Params: {params}")
            return None

    def fetchone(self, sql: str, params: tuple = ()):
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute(sql, params)
            result = cursor.fetchone()
            return result
        except sqlite3.Error as e:
            self.logger.error(f"SQL fetchone error: {e} -- Query: {sql} -- Params: {params}")
            return None

    def fetchall(self, sql: str, params: tuple = ()):
        cursor = self.__db_connection.cursor()
        try:
            cursor.execute(sql, params)
            result = cursor.fetchall()
            return result
        except sqlite3.Error as e:
            self.logger.error(f"SQL fetchall error: {e} -- Query: {sql} -- Params: {params}")
            return []
    
    def setup(self):
        self.execute("""
            CREATE TABLE IF NOT EXISTS "bracket_players" (
                "bracket_id" INTEGER NOT NULL,
                "player_id" INTEGER NOT NULL,
                "points" INTEGER,
                PRIMARY KEY("player_id","bracket_id"),
                FOREIGN KEY("bracket_id") REFERENCES "brackets"("id"),
                FOREIGN KEY("player_id") REFERENCES "players"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "bracket_rounds" (
                "bracket_id" INTEGER NOT NULL,
                "round_id" INTEGER NOT NULL,
                PRIMARY KEY("bracket_id","round_id"),
                FOREIGN KEY("bracket_id") REFERENCES "brackets"("id"),
                FOREIGN KEY("round_id") REFERENCES "rounds"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "brackets" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "state" TEXT
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "match_players" (
                "match_id" INTEGER NOT NULL,
                "player_id" INTEGER NOT NULL,
                "points" INTEGER,
                PRIMARY KEY("match_id","player_id"),
                FOREIGN KEY("player_id") REFERENCES "players"("id"),
                FOREIGN KEY("match_id") REFERENCES "matches"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "matches" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "state" TEXT,
                "host" INTEGER,
                "code" TEXT
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "players" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "mmr" INTEGER
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "round_matches" (
                "round_id" INTEGER NOT NULL,
                "match_id" INTEGER NOT NULL,
                PRIMARY KEY("round_id","match_id"),
                FOREIGN KEY("round_id") REFERENCES "rounds"("id"),
                FOREIGN KEY("match_id") REFERENCES "matches"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "rounds" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "state" TEXT
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "team_players" (
                "team_id" INTEGER NOT NULL,
                "player_id" INTEGER NOT NULL,
                PRIMARY KEY("team_id","player_id"),
                FOREIGN KEY("player_id") REFERENCES "players"("id"),
                FOREIGN KEY("team_id") REFERENCES "tournament_teams"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "tournament_brackets" (
                "tournament_id" INTEGER NOT NULL,
                "bracket_id" INTEGER NOT NULL,
                PRIMARY KEY("tournament_id","bracket_id"),
                FOREIGN KEY("bracket_id") REFERENCES "brackets"("id"),
                FOREIGN KEY("tournament_id") REFERENCES "tournaments"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "tournament_players" (
                "tournament_id" INTEGER NOT NULL,
                "player_id" INTEGER NOT NULL,
                "points" INTEGER,
                "team_id" INTEGER,
                PRIMARY KEY("tournament_id","player_id"),
                FOREIGN KEY("player_id") REFERENCES "players"("id"),
                FOREIGN KEY("tournament_id") REFERENCES "tournaments"("id"),
                FOREIGN KEY("team_id") REFERENCES "tournament_teams"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "tournament_teams" (
                "id" INTEGER NOT NULL,
                "tournament_id" INTEGER NOT NULL,
                PRIMARY KEY("id" AUTOINCREMENT),
                FOREIGN KEY("tournament_id") REFERENCES "tournaments"("id")
            )
        """)

        self.execute("""
            CREATE TABLE IF NOT EXISTS "tournaments" (
                "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                "name" TEXT,
                "region" TEXT,
                "date" TEXT,
                "team_size" INTEGER,
                "state" TEXT,
                "has_bots" INTEGER,
                "banned_characters" TEXT,
                "banned_maps" TEXT,
                "rules" TEXT,
                "prizes" TEXT,
                "is_official" INTEGER,
            )
        """)

        
