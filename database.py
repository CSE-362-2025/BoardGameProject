import sqlite3
import pathlib
from os import path
from game_manager import GameManager
from player import Player

DB_NAME_DEFAULT = "game_data.db"
DB_DIR_PATH = pathlib.Path("database")


class GameDatabase(object):

    # def __new__(cls):
    #     if not hasattr(cls, "instance"):
    #         cls.instance = super(GameDatabase, cls).__new__(cls)
    #         return cls.instance

    def __init__(self):

        # Assuming the db name doesn't change can just have static attribute

        # initialize with no connection
        self.connection = None
        self.cursor = None

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
                bilingualism INTEGER,
                fitness INTEGER,
                academics INTEGER
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
                turn_count INTEGER NOT NULL
            );
        """
        )
        self.connection.commit()

    def connect(self, db_name: str) -> bool:
        """Connect to the given DB file.

        Args:
            db_name (str): name of the DB to use

        Returns:
            bool: True if successful
        """
        name = db_name

        # use default db_name if an empty name is given
        db_path = path.join(DB_DIR_PATH, DB_NAME_DEFAULT)

        if len(name) > 0:
            # check if given name has the extension `db` and add if not
            if name[-3:] not in ".db":
                # add the extension at the end
                name += ".db"

            # create path obj
            db_path = path.join(DB_DIR_PATH, name)
            # print(f"new_path={db_path}")

        # try to connect
        print(f"about to connect to path={db_path}")
        try:
            self.connection = sqlite3.connect(db_path)
            self.cursor = self.connection.cursor()

            # initialize the table (if they don't already exist)
            self.__create_tables()

            return True

        except sqlite3.Error as e:
            print(f"GameDatabase.connect() raised exception={e}")
            return False

    def save_game(self, game_manager) -> bool:
        """Save game into the connected DB.

        Args:
            game_manager (GameManager): running instance of `GameManager`

        Returns:
            bool: True if successful, False otherwise
        """
        gm = game_manager
        try:
            print("TRYING TO SAVE TURNCOUNT")

            self.cursor(
                """
                INSERT INTO GameInfo (turn_count) VALUES (?)
                """,
                (gm.turn_count,),
            )
            self.connection.commit()
            print("TRUE")
            return True
        except sqlite3.Error as e:
            print("FALSE" + str(e))
            return False

    def load_game(self, game_manager: GameManager) -> bool:
        """Load game from the connected DB.

        Args:
            game_manager (GameManager): running instance of `GameManager`

        Returns:
            bool: True if successful, False otherwise
        """
        try:
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

                each_event_with_resp: dict[int, int] = {event_id: resp}

                # append into the player's list
                game_manager.players[player_index].events_played.append(
                    each_event_with_resp
                )

            return True
        except sqlite3.Error as e:
            # TODO: logger for error handling
            return False
        except (TypeError, ValueError) as e:
            return False
        except IndexError as e:
            return False

    def clear_database(self) -> bool:
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

    def close_connection(self) -> None:
        """Close connection to DB."""
        self.cursor.close()
        self.connection.close()


# PoC
if __name__ == "__main__":
    db = GameDatabase()
    db.connect("")
    # simulate players
    db.cursor.execute(
        """INSERT INTO Players (name, position, military, bilingualism, fitness, academics) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("Player1", 1, 1, 1, 1, 1),
    )
    db.connection.commit()
    db.cursor.execute(
        """INSERT INTO Players (name, position, military, bilingualism, fitness, academics) VALUES (?, ?, ?, ?, ?, ?)
        """,
        ("Player2", 1, 2, 2, 2, 2),
    )
    db.connection.commit()

    # simulate GameInfo
    db.cursor.execute(
        """INSERT INTO GameInfo (turn_count) VALUES (2)
        """,
    )

    # simulate events
    db.cursor.execute(
        """INSERT INTO Events (event_id, player_id) VALUES (?, ?)
        """,
        (1, 1),
    )
    db.cursor.execute(
        """INSERT INTO Events (event_id, player_id) VALUES (?, ?)
        """,
        (2, 1),
    )
    db.cursor.execute(
        """INSERT INTO Events (event_id, player_id) VALUES (?, ?)
        """,
        (3, 1),
    )
    db.connection.commit()
    db.cursor.execute(
        """INSERT INTO Events (event_id, player_id) VALUES (?, ?)
        """,
        (4, 2),
    )
    db.cursor.execute(
        """INSERT INTO Events (event_id, player_id) VALUES (?, ?)
        """,
        (5, 2),
    )
    db.cursor.execute(
        """INSERT INTO Events (event_id, player_id) VALUES (?, ?)
        """,
        (6, 2),
    )
    db.connection.commit()

    # list all events played by Player1
    res = db.cursor.execute(
        """SELECT event_id FROM Events WHERE player_id=1
        """
    )
    rows = res.fetchall()
    print(f"all events played by Player1 = {rows}")
    db.clear_database()
    db.close_connection()
