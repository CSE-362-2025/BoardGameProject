"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Manages the game and tracks when each event should occur
"""
import random
from tiles import GoodTile, BadTile, EventTile, StopTile


class GameManager:

    def __init__(self, board, players, events, ui, game_database):
        
        self.board = board
        self.players = players
        self.events = events
        self.ui = ui
        self.game_database = game_database

        self.current_player = None

        self.turn_count = 0

    # plays all logic for playing human turn
    def play_turn(self):

        roll = self.roll_dice()

        # checking if hitting a stop tile
        for tile in self.board.tiles[self.current_player.position:self.current_player.position + roll]:
            if tile.get_type() == "StopTile":
                self.current_player.position = tile.position
                break
        

        self.current_player.move(self.roll_dice())
        self.ui.display_board(self.board, self.players)

    def play_computer_turn(self):
        pass

    def start_game(self):
        self.current_player = self.players[0]
        self.ui.change_player(self.current_player)

    def end_game(self):
        pass

    def switch_turn(self):
        pass

    def roll_dice(self):
        return random.randint(1, 6)

    # used by the ui after human picks event choice
    def event_choice(self, event, choice_idx):
        pass

    # after event is acknowledged by user
    def accept_event(self, event):
        pass

    def get_random_event(self):
        return random.choice(self.events)

    def is_game_over(self):
        return self.turn_count >= 10

    def generate_good_tile_effects(self):

        return {
            "bilingual": 1,
            "athletic": 1,
            "academic": 1,
            "military": 1,
            "social": 1
        }

    def generate_bad_tile_effects(self):

        return {
            "bilingual": -1,
            "athletic": -1,
            "academic": -1,
            "military": -1,
            "social": -1
        }

