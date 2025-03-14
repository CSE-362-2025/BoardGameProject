"""
Author: Andrew
Created: 2025/02/29
Last Edited: 2025/03/02
Game manager class that controls the flow of the game and the logic of the game
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
    def play_turn(self, dice_value):

        self.current_player.has_moved = True

        roll = dice_value

        print(roll)

        # Checking if hitting a stop tile
        for tile in self.board.tiles[self.current_player.position + 1: self.current_player.position + roll + 1]:
            if tile.get_type() == "StopTile":
                print("Found StopTile")
                steps = self.board.tiles.index(tile) - self.current_player.position
                self.current_player.move(steps)
                # self.ui.display_board(self.board, self.players)
                self.handle_event(tile.event)  # Handle event for stop tile
                return  # Exit after stop tile processing

        # Move the player if not a stop tile
        self.current_player.move(roll)
        # self.ui.display_board(self.board, self.players)
        try:
            tile = self.board.tiles[self.current_player.position]
        except Exception as e:
            tile = self.board.tiles[self.board.size-1]
            self.current_player.position = self.board.size-1

        # Handle events based on tile type
        if tile.get_type() == "EventTile":
            event = self.get_random_event()
            self.handle_event(event)  # Handle event for event tile

        elif tile.get_type() in ["GoodTile", "BadTile"]:
            effects = self.generate_good_tile_effects() if tile.get_type() == "GoodTile" else self.generate_bad_tile_effects()
            self.current_player.change_stats(effects[1])
            self.ui.display_message(f"{effects[0]}")

        else:
            print(tile.get_type())
            raise Exception("Invalid tile type")
        
        
    def handle_event(self, event):
        """Handles the logic for processing an event, such as displaying the appropriate UI for decision or non-decision events."""
        if event.get_type() == "Decision":
            self.ui.display_decision_event(event)
        elif event.get_type() == "Static":
            self.ui.display_non_decision_event(event)
        else:
            print(event.get_type())
            raise Exception("Invalid event type")


    def play_computer_turn(self):
        pass

    def start_game(self):
        self.current_player = self.players[0]
        self.ui.change_current_player(self.current_player)

    def end_game(self):
        pass

    def switch_turn(self):
        self.turn_count += 1
        self.current_player = self.players[(self.turn_count) % len(self.players)]
        self.ui.change_current_player(self.current_player)
        self.ui.update(self.board, self.players)
        print(self.current_player.name)

    def roll_dice(self):
        return random.randint(1, 6)

    # used by the ui after human picks event choice
    def event_choice(self, event, choice_idx):
        event.apply_result(self.current_player, choice_idx)
        self.current_player.store_event(event, choice_idx)  # store event in player's history
        self.ui.display_board(self.board, self.players)


    # after event is acknowledged by user
    def accept_event(self, event):
        event.apply_result(self.current_player)
        self.current_player.store_event(event)  # store event in player's history
        self.ui.display_board(self.board, self.players)

    # gets a random event from the list of events that 
    # meets the criteria of the player's stats, must take into account rarity
    def get_random_event(self):
        return random.choice(self.events)

    def is_game_over(self):
        return self.turn_count >= 40

    # returns a message and stat changes in a tuple
    def generate_good_tile_effects(self):

        number = random.randint(1,5)

        if number == 1:
            return ["French Lessons! (+1 Bilingual)", {
            "bilingual": 1,
            "athletic": 0,
            "academic": 0,
            "military": 0,
            "social": 0
        }]

        elif number == 2:
            return ["Gym! (+1 Athletic)", {
            "bilingual": 0,
            "athletic": 1,
            "academic": 0,
            "military": 0,
            "social": 0
        }]

        elif number == 3:
            return ["Study! (+1 Academic)", {
            "bilingual": 0,
            "athletic": 0,
            "academic": 1,
            "military": 0,
            "social": 0
        }]

        elif number == 4:
            return ["Inspection! (+1 Military)", {
            "bilingual": 0,
            "athletic": 0,
            "academic": 0,
            "military": 1,
            "social": 0
        }]

        else:
            return ["Hang out with friends! (+1 Social)", {
            "bilingual": 0,
            "athletic": 0,
            "academic": 0,
            "military": 0,
            "social": 1
        }]

        

    def generate_bad_tile_effects(self):

        number = random.randint(1,5)

        if number == 1:
            return ["Failed French Test. (-1 Bilingual)", {
            "bilingual": -1,
            "athletic": 0,
            "academic": 0,
            "military": 0,
            "social": 0
        }]

        elif number == 2:
            return ["Failed PPT Run. (-1 Athletic)", {
            "bilingual": 0,
            "athletic": -1,
            "academic": 0,
            "military": 0,
            "social": 0
        }]

        elif number == 3:
            return ["Failed Math Test. (-1 Academic)", {
            "bilingual": 0,
            "athletic": 0,
            "academic": -1,
            "military": 0,
            "social": 0
        }]

        elif number == 4:
            return ["5s and Gs. (-1 Military)", {
            "bilingual": 0,
            "athletic": 0,
            "academic": 0,
            "military": -1,
            "social": 0
        }]

        else:
            return ["Said Something Dumb in Class. (-1 Social)", {
            "bilingual": 0,
            "athletic": 0,
            "academic": 0,
            "military": 0,
            "social": -1
        }]

