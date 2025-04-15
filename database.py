import sqlite3
from os import path
import pathlib

DB_NAME_DEFAULT = "game_data.db"
DB_DIR_PATH = pathlib.Path("database")

class GameDatabase:

    def __init__(self):
        
        # Assuming the db name doesn't change can just have static attribute
        self.connection = sqlite3.connect('')
        self.cursor = self.connection.cursor()

    def __create_tables(self) -> None:
        """Run queries to create tables if they don't already exist
        into the connected DB.

        Connection to the valid DB must be made before.
        """
        if self.connection is None:
            print("GameDatabase.__create_tables(): must have DB connected!")
            return

        # CREATE `Players` table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Players (
                player_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                position INTEGER,
                military INTEGER,
                bilingual INTEGER,
                athletic INTEGER,
                academic INTEGER,
                social INTEGER,
                has_moved BOOLEAN,
                branch BOOLEAN,
                next_pos INTEGER,
                on_alt_path BOOLEAN
            );
        """
        )
        self.connection.commit()

        # CREATE `Events` table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS Events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id INTEGER,
                player_id INTEGER,
                response INTEGER,
                FOREIGN KEY (player_id) REFERENCES Players(player_id)
            );
        """
        )
        self.connection.commit()

        # CREATE `GameInfo` table
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS GameInfo (
                game_info_id INTEGER PRIMARY KEY AUTOINCREMENT,
                turn_count INTEGER NOT NULL,
                current_player_index INTEGER NOT NULL,
                is_game_over BOOLEAN
            );
        """
        )
        self.connection.commit()

    def connect(self, db_name):
        name = db_name
        db_path = path.join(DB_DIR_PATH, DB_NAME_DEFAULT)

        if len(name) > 0:
            # if file has .db extension
            if name[-3:] not in ".db":
                name += ".db"
                db_path = path.join(DB_DIR_PATH, DB_NAME_DEFAULT)

        print(f"trying to connect to path={db_path}")
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()

            # initialize the table (if they don't already exist)
            self.__create_tables()
            return True

        except sqlite3.Error as e:
            print(f"GameDatabase.connect() raised exception={e}")
            return False    

    # return true is success, false otherwise
    def save_game(self, game_manager):

        if game_manager is None:
            return False

        try:
            # clear DB first
            if not self.clear_database():
                # clear_database failed
                print("GameDatabase.save_game(): failed to clear DB before saving")
                return False

            # save GameInfo
            current_player_index: int = game_manager.players.index(
                game_manager.current_player
            )
            self.cursor.execute(
                """
                INSERT INTO GameInfo (turn_count, current_player_index, is_game_over)
                VALUES (?, ?, ?)
                """,
                (
                    game_manager.turn_count,
                    current_player_index,
                    int(game_manager.is_game_over()),
                ),
            )
            self.connection.commit()

            # save all players into DB
            for each_player_index, each_player in enumerate(game_manager.players):
                self.cursor.execute(
                    """
                    INSERT INTO Players (
                        name, position, military, bilingual, athletic, academic, social, has_moved, branch, next_pos, on_alt_path
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        each_player.name,
                        each_player.position,
                        each_player.stats["military"],
                        each_player.stats["bilingual"],
                        each_player.stats["athletic"],
                        each_player.stats["academic"],
                        each_player.stats["social"],
                        int(each_player.has_moved),
                        int(each_player.branch),
                        each_player.next_pos,
                        int(each_player.on_alt_path),
                    ),
                )
                self.connection.commit()

                # save all events played by the players into DB
                for each_event in each_player.events_played:
                    resp = each_event[1]
                    if resp is None:
                        resp = "NULL"
                    self.cursor.execute(
                        """
                        INSERT INTO Events (event_id, player_id, response)
                        VALUES (?, ?, ?)
                        """,
                        (
                            int(each_event[0]),
                            int(each_player_index),
                            resp
                        ),
                    )
                    self.connection.commit()

            return True
        except sqlite3.Error as e:
            print(f"GameDatabase.save_game(): unexpected exception = {e}")
            return False

    def load_game(self, game_manager):
        """Load game from the connected DB.

        Args:
            game_manager (GameManager): running instance of `GameManager`

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            print("Trying to load game")
            # grab game_info from DB
            db_gameinfo_rows: list[tuple] = self.cursor.execute(
                """SELECT turn_count FROM GameInfo
                """
            ).fetchall()
            # overwrite into game_manager

            game_manager.turn_count = int(db_gameinfo_rows[0][0])

            # grab players info and into game_manager's list of players
            db_player_rows: list[tuple] = self.cursor.execute(
                """SELECT name, position, bilingual, athletic, military, social
                FROM Players
                """
            ).fetchall()
            # initialize new Player obj with info from DB
            for i, each_player in enumerate(game_manager.players):
                # ordered by ID <-> index
                each_row = db_player_rows[i]

                # overwrite player's obj with data from DB
                each_player.name = str(each_row[0])
                each_player.position = int(each_row[1])
                each_player.stats["bilingual"] = int(each_row[2])
                each_player.stats["athletic"] = int(each_row[3])
                each_player.stats["military"] = int(each_row[4])
                each_player.stats["social"] = int(each_row[5])

                # TODO: load other attributes (has_moved, next_pos, ...)

                # reset events_played list
                each_player.events_played = []

            curr_index = self.cursor.execute(
                """
                SELECT current_player_index FROM GameInfo
                """
            ).fetchone()

            


            # grab events from DB
            db_event_rows: list[tuple] = self.cursor.execute(
                """SELECT player_id, event_id, response
                FROM Events
                """
            ).fetchall()

            # append events played by a player (dict)
            for each_event_row in db_event_rows:
                # SQL IDs starts at one
                player_index: int = int(each_event_row[0]) - 1
                event_id: int = each_event_row[1]
                resp: int = each_event_row[2]

                each_event_with_resp: tuple[int] = (event_id,resp)


                # append into the player's list
                game_manager.players[player_index].events_played.append(
                    each_event_with_resp
                )
                game_manager.players[player_index].events_played_id.append(
                    event_id                    
                )
            return True
        except sqlite3.Error as e:
            # TODO: logger for error handling
            print(f"sqlite3 error: {e}")
            return False
        except (TypeError, ValueError) as e:
            print(f"type error, value error: {e}")
            return False
        except IndexError as e:
            print(f"index error: {e}")
            return False

    def clear_database(self):
        """Clear any saved game states from the connected DB.

        Args:
            game_manager (GameManager): running instance of `GameManager`

        Returns:
            bool: True if successful, False otherwise
        """

        try:
            self.cursor.execute(
                """
                DELETE FROM Players;
            """
            )
            self.cursor.execute(
                """
                DELETE FROM GameInfo;
            """
            )
            self.cursor.execute(
                """
                DELETE FROM Events;
            """
            )
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"FAILED: {e}")
            return False

    def close_connection(self):
        pass

if __name__ == "__main__":
    db = GameDatabase()
    db.connect("DB_NAME_DEFAULT")
