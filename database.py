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
