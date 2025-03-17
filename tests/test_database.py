import os
# to import from `database.py` file from parent directory
import sys
import unittest
from random import randint
from unittest.mock import Mock

# to import from `database.py` file from parent directory only when inside `tests` dir
if os.getcwd().endswith(("tests", "tests/", "tests\\")):
    sys.path.append("../")
else:
    sys.path.append("../BoardGameProject")

from database import DB_DIR_PATH, DB_NAME_DEFAULT, GameDatabase


class TestGameDataBase(unittest.TestCase):

    test_db_name_default: str = DB_NAME_DEFAULT

    def setUp(self):
        self.db = GameDatabase()
        self.mock_gm = self.__create_mock_game_manager_instance()

    def tearDown(self):
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

            self.db.close_connection()

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

        # simulate players
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

            # create random events played for each player
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
        res = self.db.save_game(game_manager=self.mock_gm)
        self.assertTrue(res)

        # TODO: test against the saved DB file

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


if __name__ == "__main__":
    unittest.main()
