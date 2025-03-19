import sqlite3
import pathlib
from os import path
from game_manager import GameManager

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

    def save_game(self, game_manager: GameManager) -> bool:
        """Save game into the connected DB.

        Args:
            game_manager (GameManager): running instance of `GameManager`

        Returns:
            bool: True if successful, False otherwise
        """
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
                    int(game_manager.is_game_over),
                ),
            )

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

                # save all events played by the players into DB
                for each_event_dict in each_player.events_played:
                    each_event_id: int = int(list(each_event_dict.keys())[0])
                    self.cursor.execute(
                        """
                        INSERT INTO Events (event_id, player_id, response)
                        VALUES (?, ?, ?)
                        """,
                        (
                            each_event_dict,
                            each_player_index,
                            int(each_event_dict[each_event_id]),
                        ),
                    )

            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print("FALSE" + str(e))
            return False

    def load_game(self, game_manager) -> bool:
        """Load game from the connected DB.

        Args:
            game_manager (GameManager): running instance of `GameManager`

        Returns:
            bool: True if successful, False otherwise
        """

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
