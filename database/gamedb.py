import sqlite3
from typing import Any

DB_NAME = "game_data.db"


class GameDataBase:
    def __init__(self):
        # TODO: make this singleton
        # self.conn = self.get_connection()
        pass

    def get_connection(self):
        return sqlite3.connect(DB_NAME)

    def initialize_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE iF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT
            name TEXT NOT NULL,
            position INTEGER
            )
        """
        )

        conn.commit()
        conn.close()

    def create_player(self, name: str) -> None:
        """Create player with given name.

        Args:
            name (str): name of the players
        """
        conn = self.get_connection()
        conn.cursor().execute(f"INSERT INTO players (name) VALUES {name}")
        conn.commit()
        conn.close()

    def get_player(self, player_id: int) -> Any:
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id, name, score, level FROM players WHERE id = {player_id}"
        )
        row = cursor.fetchone()
        conn.close()

        return row

    def update_player_position(self, player_id, new_position) -> None:
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"UPDATE players SET position = {new_position} WHERE id = {player_id}"
        )
        conn.commit()
        conn.close()
