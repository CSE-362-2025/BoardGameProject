import sqlite3
from typing import Any

DB_NAME = "database/game_data.db"


class GameDataBase(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(GameDataBase, cls).__new__(cls)
            return cls.instance

    def _get_connection(self):
        return sqlite3.connect(DB_NAME)

    def initialize_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
        CREATE TABLE iF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            position INTEGER
            )

        CREATE TABLE iF NOT EXISTS stats (
            player_id INTEGER FOREIGN KEY REFERENCES players(id)
            military INTEGER,
            bilingualism INTEGER,
            fitness INTEGER,
            academics INTEGER
        """
        )

        conn.commit()
        conn.close()

    def create_player(self, name: str) -> None:
        # also save the stats
        """Create player with given name.

        Args:
            name (str): name of the players
        """
        conn = self._get_connection()
        conn.cursor().execute(f"INSERT INTO players (name) VALUES ('{name}')")
        conn.commit()
        conn.close()

    def get_player(self, player_id: int) -> Any:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT id, name, position FROM players WHERE id = {player_id}")
        row = cursor.fetchone()
        conn.close()

        return row

    def update_player_position(self, player_id, new_position) -> None:
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"UPDATE players SET position = {new_position} WHERE id = {player_id}"
        )
        conn.commit()
        conn.close()

    # update stat
    def update_stats(
        self, player_id: int, military=0, bilingualism=0, fintess=0, academics=0
    ):
        conn = self._get_connection()
        cursor = conn.cursor()

        curr_stat = get_stat()

        curosor.execute()

    # get stat
    def get_stat(self, player_id: int):
        """

        Args:
            player_id (int): player id

        Returns:
            row
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"SELECT id, military, bilingualism, fitness, academics FROM players WHERE id = {player_id}"
        )
        row = cursor.fetchone()
        conn.close()

        return row
