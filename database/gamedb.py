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
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            military INTEGER,
            bilingualism INTEGER,
            fitness INTEGER,
            academics INTEGER,            
            position INTEGER 
            );
        """
        )
        conn.commit()
        conn.close()

    def create_player(self, name: str, military, bilingualism, fitness, academics) -> None:
        """
        Create player with given name. You can add stat points to each of the category: military, bilingualism, fitness and academics

        Args:
            name (str): name of the player created 
            military (int): stat value added into military 
            bilingualism (int): stat value added into bilingualism 
            fitness (int): stat value added into fitness 
            academics (int): stat value added into academics 
            
        """
        conn = self._get_connection()
        conn.cursor().execute(f"INSERT INTO players (name, military, bilingualism, fitness, academics) VALUES ('{name}', {military}, {bilingualism}, {fitness}, {academics});")
        conn.commit()
        conn.close()

    def get_player(self, player_id: int) -> Any:
        """
        gets all stats of a specific player

        Args:
            player_id (int): id of the players

        Returns:
            tuple: values of a specific row
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM players WHERE id = {player_id};")
        row = cursor.fetchone()
        conn.close()
        
        return row

    def update_player_position(self, player_id, new_position) -> None:
        """
        updates the position of a player given their id and new_position. 

        Args:
            player_id (int): id of the player
            new_position (int): the new position the player moved to
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute(
            f"UPDATE players SET position = {new_position} WHERE id = {player_id}"
        )
        conn.commit()
        conn.close()

    def get_stats(self, player_id: int):
        """
        Converts the given row of a player to a list for updating purposes
        Args:
            player_id (int): id of the player 

        Returns:
            row (list): list of all stats of current player
        """
        conn = self._get_connection()
        row = self.get_player(player_id=player_id)
        list_row = list(row)
        conn.close()
        return list_row
 
    def update_stats(self, player_id: int, military=0, bilingualism=0, fitness=0, academics=0): 
        """
        Updates the stats of a player
        Args:
            player_id (int): the current player id
            military (int, optional): military value that will be added to current stat value. Defaults to 0.
            bilingualism (int, optional): bilingualism value that will be added to current stat value. Defaults to 0.
            fitness (int, optional): fitness value that will be added to current stat value. Defaults to 0.
            academics (int, optional): academics value that will be added to current stat value. Defaults to 0.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        curr_stat = self.get_stats(player_id)
        curr_stat[2] = curr_stat[2] + military
        curr_stat[3] = curr_stat[3] + bilingualism
        curr_stat[4] = curr_stat[4] + fitness
        curr_stat[5] = curr_stat[5] + academics
 
        cursor.execute(
            f"UPDATE players SET military={curr_stat[2]}, bilingualism={curr_stat[3]}, fitness={curr_stat[4]}, academics={curr_stat[5]} where id={player_id}"
        )
        conn.commit()
        conn.close()

       
if __name__ == '__main__':
    # testing purposes
    gb = GameDataBase()
    gb.initialize_db()
    #gb.create_player("JOHN JOE", 5, 6, 1, 3)
    print(gb.get_player(4))
    gb.update_stats(4,8,3,2,1) 
    gb.update_player_position(4,5)
    print(gb.get_player(4))