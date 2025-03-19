import os
import sqlite3
import sys
import unittest
from pathlib import Path
from random import randint
from unittest.mock import Mock

if os.getcwd().endswith(("tests", "tests/", "tests\\")):
    # inside tests directory, move up
    dest_path = Path(os.getcwd()).parent.absolute()
    print(f"changing CWD {os.getcwd()} -> {dest_path}")
    os.chdir(dest_path)

# add parent (project's root) dir to PATH
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(f"appended to PATH: {(os.path.dirname(os.path.dirname(__file__)))}")

from database import DB_DIR_PATH, DB_NAME_DEFAULT, GameDatabase


class TestGameDataBase(unittest.TestCase):

    test_db_name_default: str = DB_NAME_DEFAULT

    def setUp(self):
        self.db = GameDatabase()
        self.db.connect(TestGameDataBase.test_db_name_default)
        self.mock_gm = self.__create_mock_game_manager_instance()

    def tearDown(self):
        self.db.close_connection()

        del self.db
        self.db = None
        del self.mock_gm
        self.mock_gm = None

        # delete the default DB files created during this test case
        db_path = os.path.join(DB_DIR_PATH, TestGameDataBase.test_db_name_default)
        if os.path.exists(db_path):
            # delete this file
            os.remove(db_path)

    @classmethod
    def tearDownClass(cls):
        # delete all DB files created
        ls = os.listdir(DB_DIR_PATH)
        for each_item in ls:
            if each_item.endswith(".db"):
                os.remove(os.path.join(DB_DIR_PATH, each_item))

    def __test_conn(self, db_name: str):
        """Helper method to test GameDatabase.connect() by creating a DB file with given name.

        Args:
            db_name (str): name of the DB
        """
        try:
            res = self.db.connect(db_name)
            self.assertTrue(res)

            # db is now closed inside `tearDown`
            # self.db.close_connection()

            # delete the DB files created during this test case
            db_path = os.path.join(DB_DIR_PATH, db_name)
            if os.path.exists(db_path):
                # delete this file
                os.remove(db_path)
                print(f"deleted {db_path}")

        except Exception as e:
            self.fail(f"unwanted exception occurred: {e}")

    def __create_mock_game_manager_instance(self) -> Mock:
        mock_gm: Mock = Mock()
        mock_gm.board = "board"
        mock_gm.turn_count = 10
        mock_gm.events = ["event1", "event2"]
        mock_gm.ui = "ui"
        mock_gm.game_database = "game_database"
        mock_gm.players: list[Mock] = []

        # simulate 4 players
        for i in range(1, 5):
            mock_player: Mock = Mock()
            mock_player.name = f"player_{i}"
            mock_player.position = randint(1, 10)
            mock_player.status: dict[str, int] = {
                "bilingual": randint(1, 10),
                "athletic": randint(1, 10),
                "academic": randint(1, 10),
                "military": randint(1, 10),
                "social": randint(1, 10),
            }

            mock_player.events_played: list[dict[Mock, int]] = []

            # create 5 random events played for each player
            for j in range(1, 5):
                mock_event: Mock = Mock()
                mock_event.name: str = f"mock_event_{j}"
                mock_event.id: int = randint(1, 10)

                mock_player.events_played.append({mock_event: randint(1, 3)})

            mock_gm.players.append(mock_player)

        return mock_gm

    def __get_mock_player_by_name(self, player_name: str) -> Mock | None:
        """Return a mock Player object that has the given `player_name`

        Args:
            player_name (str): target player_name

        Returns:
            Mock | None: mock player object with simulated data, None if DNE
        """
        for each_player in self.mock_gm.players:
            if player_name == each_player.name:
                return each_player
        return None

    def test_connect_with_valid_name_without_extension(self):
        """Test if connect() is successful with a given valid `db_name`
        without the `.db` extension at the end of the file name.
        """
        valid_name: str = "my_data"
        self.__test_conn(valid_name)

    def test_connect_with_valid_name_with_extension(self):
        valid_name: str = "my_data.db"
        self.__test_conn(valid_name)

    def test_save_game_valid(self):
        """Test if save_game() properly save game data into DB.
        **This assumes connect() passed the test.**
        """
        try:

            # create connection to default name for this test
            conn = sqlite3.connect(self.test_db_name_default)
            cur = conn.cursor()

            res = self.db.save_game(game_manager=self.mock_gm)
            self.assertTrue(res)

            # * check for Players table

            # fetch rows from `Players` table
            rows_players = cur.execute(
                """SELECT * FROM Players
                """
            ).fetchall()

            # should have 4 rows
            self.assertEqual(4, len(rows_players))

            # get all names from DB
            expected_names: list[str] = [each.name for each in self.mock_gm.players]
            rows_player_names = cur.execute(
                """SELECT name FROM Players
                """
            ).fetchall()

            # check if all four expected player names are inside DB
            self.assertListEqual(
                expected_names, [str(each[0]) for each in rows_player_names]
            )

            # go through all players to compare stats (test passed above)
            for each_expected_name in expected_names:
                # grab actual player info from DB
                actual_player_info_row: list[tuple] = cur.execute(
                    """SELECT position, military, bilingual, fitness, academic, social
                    FROM Players WHERE name = ?
                    """,
                    (each_expected_name),
                ).fetchall()

                # no duplicate name allowed
                self.assertEqual(1, len(actual_player_info_row))

                # grab expected player info to test it below
                expected_player: Mock = self.__get_mock_player_by_name(
                    each_expected_name
                )
                self.assertIsNotNone(expected_player)
                expected_info: tuple = (
                    expected_player.position,
                    expected_player.status["military"],
                    expected_player.status["bilingual"],
                    expected_player.status["fitness"],
                    expected_player.status["academic"],
                    expected_player.status["social"],
                )

                # check if expected player info is same as actual
                self.assertTupleEqual(expected_info, actual_player_info_row[0])

                # * done checking `Players` table

                # * check for `Events` table

                # get all events info for current `each_expected_name`
                actual_event_row: list[tuple] = cur.execute(
                    """SELECT event_id, player_id, response
                    FROM Events
                    WHERE player_id IN
                    (
                        SELECT player_id FROM Players
                        WHERE name = ?
                    )
                    """,
                    (each_expected_name),
                ).fetchall()

                # check if have 5 events played
                self.assertEqual(5, len(actual_event_row))

                # grab expected event info to test it below
                expected_event_info: list[tuple] = []
                for each_event_mock_obj in list(expected_player.events_played.keys()):
                    each_event_info_tup: tuple = (
                        each_event_mock_obj.id,
                        int(expected_player.name.split("_")[1]),
                        int(expected_player.events_played[each_event_mock_obj]),
                    )
                    expected_event_info.append(each_event_info_tup)

                # compare expected and actual events info
                self.assertTupleEqual(expected_event_info, actual_event_row)

                # * done checking `Events` table

                # * check for `GameInfo` table

                actual_gameinfo_row: list[tuple] = cur.execute(
                    """SELECT turn_count FROM GameInfo
                    """
                ).fetchall()

                # check if only one turn_count (by design)
                self.assertEqual(1, len(actual_gameinfo_row))

                # grab expected game_info
                expected_game_info_row: tuple = self.mock_gm.turn_count

                # compare turn count
                self.assertTupleEqual(expected_game_info_row, actual_gameinfo_row)

                # * done checking `GameInfo` table

            cur.close()
        except sqlite3.Error as e:
            self.fail(f"unexpected exception thrown: {e}")

        finally:
            # close conn
            if conn:
                conn.close()

    def test_save_game_invalid_none(self):
        res = self.db.save_game(None)
        self.assertFalse(res)

    def test_save_and_load(self):
        self.db.save_game(self.mock_gm)

        # create randomized mock gm instance to load into
        rand_gm = self.__create_mock_game_manager_instance()
        # load game from DB file into `rand_gm`
        res = self.db.load_game(rand_gm)

        self.assertTrue(res)

        self.assertDictEqual(vars(rand_gm), vars(self.mock_gm))

    def test_clear_database(self):

        # write data into DB
        self.db.save_game(self.mock_gm)

        res = self.db.clear_database()

        self.assertTrue(res)

        # check if table has no rows
        try:
            conn = sqlite3.connect(self.test_db_name_default)
            cursor = conn.cursor()

            # check if Players table is empty
            player_rows = cursor.execute(
                """SELECT * FROM Players
                """
            ).fetchall()
            self.assertEqual(0, len(player_rows))

            # check if Events table is empty
            event_rows = cursor.execute(
                """SELECT * FROM Events
                """
            ).fetchall()
            self.assertEqual(0, len(event_rows))

            # check if GameInfo table is empty
            gameinfo_rows = cursor.execute(
                """SELECT * FROM GameInfo
                """
            ).fetchall()
            self.assertEqual(0, len(gameinfo_rows))

            cursor.close()
        except sqlite3.Error as e:
            self.fail(f"unexpected exception thrown: {e}")
        finally:
            if conn:
                conn.close()


if __name__ == "__main__":
    unittest.main()
