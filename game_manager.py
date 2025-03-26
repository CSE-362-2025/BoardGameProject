"""
Author: Andrew
Created: 2025/02/29
Last Edited: 2025/03/02
Game manager class that controls the flow of the game and the logic of the game
"""

import random
from board import Board
from tiles import Tile, StopTile
from player import Player
from event import Event
import json


class GameManager:

    def __init__(self, ui, game_database):
        
        self.board = None
        self.players = None
        self.events = None
        self.ui = ui
        self.game_database = game_database
        self.year = 0

        self.current_player = None
        self.turn_count = 0

    # plays all logic for playing human turn
    def play_turn(self, dice_value):

        self.current_player.has_moved = True

        roll = dice_value

        if self.current_player.branch:
            self.current_player.branch = False
            self.current_player.position = self.current_player.next_pos
            self.current_player.on_alt_path = True
            

        # Checking if hitting a stop tile
        for tile in self.board.tiles[self.current_player.position + 1: self.current_player.position + roll + 1]:
            if tile.get_type() == "StopTile":
                print("Found StopTile")
                steps = tile.position - self.current_player.position
                self.current_player.move(steps)
                if len(tile.paths) > 1:
                    self.current_player.branch = True

                self.ui.display_stoptile_event(tile.event)
                return  # Exit after stop tile processing

        # Move the player if not a stop tile
        self.current_player.move(roll)

        print(f"Current Player Position: {self.current_player.position}")

        tile = self.board.get_tile(self.current_player.position)

        if not tile and self.current_player.on_alt_path:
            self.current_player.on_alt_path = False
            self.current_player.position -= 100  # Puts the position back on "main" path
            tile = self.board.get_tile(self.current_player.position)
            print(tile.position, self.current_player.position)

        if not tile:          
            tile = self.board.tiles[self.board.size-1]
            self.current_player.position = self.board.size-1

        # Handle events based on tile type
        if tile.get_type() == "EventTile":
            event = self.get_random_event()
            self.ui.display_decision_event(event)

        elif tile.get_type() in ["GoodTile", "BadTile"]:
            effects = self.generate_good_tile_effects() if tile.get_type() == "GoodTile" else self.generate_bad_tile_effects()
            self.current_player.change_stats(effects[1])
            self.ui.display_message(f"{effects[0]}")

        else:
            print(tile.get_type())
            raise Exception("Invalid tile type")


    def play_computer_turn(self):
        pass

    def start_game(self):
        print("Starting")
        events = self.get_events(0)
        self.events = events
        self.board = self.get_board(0)
        self.players = self.get_players()
        self.current_player = self.players[0]
        self.ui.change_current_player(self.current_player)
    
    def get_events(self, year):
             # Create events
        with open("game_objects/events.json") as file:
            events_raw = json.load(file)
        
        events = []
        for event in events_raw:
            events.append(Event(event['name'], event['description'], 
                                    event['choices'], event['rarity'],
                                    event['phase']))
        return events

    def get_board(self, year):
        boards = []
        with open("game_objects/boards.json") as file:
            boards_raw = json.load(file)
    
        board_raw = boards_raw[0]
        tiles = []
        for tile in board_raw['tiles']:
            if tile['tile_type'] == "StopTile":
                event_raw = tile['event']
                if event_raw:
                    event = Event(event_raw['name'], event_raw['description'], event_raw['choices'])
                else:
                    event = None
                tiles.append(StopTile(tile['position'], tile['screen_position'],event, tile['paths']))
            else:
                tiles.append(Tile(tile['position'], tile['screen_position'], tile['tile_type']))
    
        boards.append(Board(tiles, board_raw['year']))
        board = boards[0]
        return board

    def get_players(self):
        
        # Create players
        players = [
            Player("Player 1", (50, 200, 50), image="Resources/test_meeple.png"),
            Player("Player 2", (50, 200, 200),),
            Player("Player 3", (200, 200, 200),),
            Player("Player 4", (200, 200, 50),),
        ]
        return players

    
    def end_game(self):
        pass

    def switch_turn(self):
        self.turn_count += 1
        self.current_player = self.players[(self.turn_count) % len(self.players)]
        self.ui.change_current_player(self.current_player)
        self.ui.update()
        print(self.current_player.name)

    def roll_dice(self):
        return random.randint(1, 6)

    # used by the ui after human picks event choice
    def event_choice(self, event, choice_idx):
        event.apply_result(self.current_player, choice_idx)
        self.current_player.store_event(event, choice_idx)  # store event in player's history
        self.ui.display_board(self.board, self.players)

    def branching_event_choice(self, event, choice_idx):
        event.apply_result(self.current_player, choice_idx)
        pos = self.current_player.position
        self.current_player.next_pos = (self.board.tiles[pos].paths[choice_idx-1]) - 1
        self.current_player.store_event(event, choice_idx)  # store event in player's history
        self.ui.display_board(self.board, self.players)

    # gets a random event from the list of events that 
    # meets the criteria of the player's stats, must take into account rarity
    def get_random_event(self, cook_results=False): 
        number = random.randint(1,20)
        i=0    # avoid infinate loop

        # common 75%
        if number >= 1 and number <= 15:
            while i < 500:
                event = random.choice(self.events)
                if event.rarity != 2 and self.board.year not in event.phase:
                    i += 1
                    continue
                else:
                    break

        # rare 20%
        elif number >= 16 and number <= 19:
            while i < 500:
                event = random.choice(self.events)
                if event.rarity != 1 and self.board.year not in event.phase:
                    i += 1
                    continue
                else:
                    break

        # super rare 5%
        else:
            while i < 500:
                event = random.choice(self.events)
                if event.rarity != 0 and self.board.year not in event.phase:
                    i += 1
                    continue
                else:
                    break

        

    def is_game_over(self):
        return self.turn_count >= 40

    # returns a message and stat changes in a tuple
    def generate_good_tile_effects(self):

        number = random.randint(1,5)

        if number == 1:
            return ["French Lessons! (+1 Biligual)", {
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

