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
        """
        )
        cursor.execute(
        """
        CREATE TABLE iF NOT EXISTS stats (
            player_id INTEGER,
            military INTEGER,
            bilingualism INTEGER,
            fitness INTEGER,
            academics INTEGER,
            FOREIGN KEY(player_id) REFERENCES players(id)
            )
        """
        )
        conn.commit()
        conn.close()

    def create_player(self, name: str, military, bilingualism, fitness, academics) -> None:
        """Create player with given name.

        Args:
            name (str): name of the players
            military (int): stat value added into military 
            bilingualism (int): stat value added into bilingualism 
            fitness (int): stat value added into fitness 
            academics (int): stat value added into academics 
            
        """
        conn = self._get_connection()
        conn.cursor().execute(f"INSERT INTO players (name) VALUES ('{name}')")
        # TODO: Might need to specify player ID
        conn.cursor().execute(f"INSERT INTO stats (military, bilingualism, fitness, academics) VALUES ({military}, {bilingualism}, {fitness}, {academics})")
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
    def update_stats (self, player_id: int, military=0, bilingualism=0, fintess=0, academics=0): 
        conn = self._get_connection()
        cursor = conn.cursor()
        curr_stat = get_stat()

        new_military = curr_stat[1] + military
        new_bilingualism = curr_stat[2] + bilingualism
        new_fitness = curr_stat[3] + fitness
        new_academics = curr_stat[4] + academics
 
        cursor.execute(
            f"UPDATE stats SET military={new_military}, bilingualism={new_bilingualism}, new_fitness={new_fitness}, academics={new_academics}"
        )

        conn.commit()
        conn.close()

    # get stat
    def get_stat(self, player_id: int):
        """

        Args:
            player_id (int): player id 

        Returns:
            row (list): list of all stats of current player
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT player_id, military, bilingualism, fitness, academics FROM stats WHERE player_id = {player_id}")
        row = cursor.fetchone()
        conn.close()

        return row
        
if __name__ == '__main__':
    gb = GameDataBase()
    gb.initialize_db()
    gb.create_player("Bob Smith", 5, 6, 1, 3)
    print(gb.get_stat(1))

    