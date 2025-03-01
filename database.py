import sqlite3

class GameDatabase:

    def __init__(self):
        
        # Assuming the db name doesn't change can just have static attribute
        self.connection = sqlite3.connect('')
        self.cursor = self.connection.cursor()

    def connect(db_name):
        pass
    
    # return true is success, false otherwise
    def save_game(self, game_manager):
        pass

    def load_game(self, game_manager):
        pass

    def clear_database(self):
        pass

    def close_connection(self):
        pass


