import unittest

# to import from `database.py` file from parent directory
import sys

sys.path.append("../BoardGameProject")

from database import GameDatabase


class TestGameDataBase(unittest.TestCase):

    def setUp(self):
        self.db = GameDatabase()
        print("setup called")

    def tearDown(self):
        self.db = None
        del self.db

    def _test_conn(self, db_name: str):
        """Helper method to test GameDatabase.connect()

        Args:
            db_name (str): name of the DB
        """
        try:
            res = self.db.connect(db_name)
            self.assertTrue(res)

            # TODO: delete the DB files created

        except Exception as e:
            self.fail(f"unwanted exception occurred: {e}")

    def test_connect_with_valid_name_without_extension(self):
        """Test if connect() is successful with a given valid `db_name`
        without the `.db` extension at the end of the file name.
        """
        print(self.db)
        valid_name: str = "my_data"
        self._test_conn(valid_name)

    def test_connect_with_valid_name_with_extension(self):
        print(self.db)
        valid_name: str = "my_data.db"
        self._test_conn(valid_name)


if __name__ == "__main__":
    unittest.main()
