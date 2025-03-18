"""
Author: Bottom Six
Created: 2025/02/29
Last Edited: 2025/03/18
Game manager class that controls the flow of the game and the logic of the game
"""

import random
import board as boardClass
from tiles import GoodTile, BadTile, EventTile, StopTile
from player import Player
from event import DecisionEvent, StaticEvent
import json


class GameManager:

    def __init__(self, ui, game_database):
        self.board = None
        self.players = None
        self.events = None
        self.ui = ui
        self.game_database = game_database

        self.current_player = None
        self.turn_count = 0

    # plays all logic for playing human turn
    def play_turn(self, dice_value):

        self.current_player.has_moved = True
        roll = dice_value

        print(roll)
        path = []
        # Checking if hitting a stop tile
        for tile in self.board.tiles:
            if tile.path == self.current_player.path:
                path.append(tile)
                if self.current_player.position < tile.ID < self.current_player.position + roll + 1:
                    if tile.get_type() == "StopTile":
                        print("Found StopTile")
                        steps = self.board.tiles.index(tile) - self.current_player.position
                        self.current_player.move(steps)
                        # self.ui.display_board(self.board, self.players)
                        self.handle_event(tile.event)  # Handle event for stop tile
                        return  # Exit after stop tile processing

        # Move the player if not a stop tile
        self.current_player.move(roll)
        try:
            try:
                for pos in path:
                    #first attempt to go to next tile on path
                    if pos.ID == self.current_player.position:
                        tile = pos
                        break
            except Exception:
                #no tile on path - paths have merged (no maps have reachable next split)
                self.current_player.path = 0 #returns player to main path
                for pos in self.board.tiles:
                    if pos.ID == self.current_player.position:
                        tile = pos
                        break
        except Exception as e:
            #gone past the end of the board
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
        print("Starting")
        events = self.get_events(0)
        self.events = events[0]
        self.board = self.get_board(0, events[1])
        self.players = self.get_players()
        self.current_player = self.players[0]
        self.ui.change_current_player(self.current_player)

    def get_events(self, year):
         # Create events
        with open("game_objects/events.json") as file:
            events_raw = json.load(file)
            events = []
            for event in events_raw:
                if event['type'] == "Decision":
                    events.append(DecisionEvent(event['name'], event['description'], 
                                                event['criteria'], event['choices'],
                                                event['rarity']))

                elif event['type'] == "Static":
                    events.append(StaticEvent(event['name'], event['description'], 
                                                event['criteria'], event['result'],
                                                event['rarity']))
                    
            event_stoptile_1 = StaticEvent("StopTile 1", "PPT! (+2 Athletic)", None, {
                        "bilingual": 0,
                        "athletic": 2,
                        "military": 0,
                        "academic": 0,
                        "social": 0,
                    }, 0)
            event_stoptile_2 = StaticEvent("StopTile 2", "Exams! (+3 Academic)", None, {
                        "bilingual": 0,
                        "athletic": 0,
                        "military": 0,
                        "academic": 3,
                        "social": 0,
                    }, 0)
            event_stoptile_3 = StaticEvent("StopTile 2", "Exams! (+3 Academic)", None, {
                        "bilingual": 0,
                        "athletic": 0,
                        "military": 0,
                        "academic": 3,
                        "social": 0,
                    }, 0)
            return (events, (event_stoptile_1,event_stoptile_2,event_stoptile_3)) 

    def get_board(self, year, stop_events):
        match year:
            case 0:
                # Create board with tiles
                tiles = [
                    GoodTile(0,(10, 10)), BadTile(1,(25, 10)), GoodTile(2,(40, 10)), BadTile(3,(55, 10)), EventTile(4,(70, 10)),
                    GoodTile(5,(85, 10)), BadTile(6,(90, 20)), StopTile(7,(80, 25), stop_events[0]),
                    GoodTile(8,(70, 25)), BadTile(9,(60, 25)), GoodTile(10,(50, 25)), BadTile(11,(40, 25)), EventTile(12,(30, 25)), BadTile(13,(20, 35)), EventTile(14,(20,45)), #route 0
                    GoodTile(8,(80, 40),1), BadTile(9,(80, 50),1), GoodTile(10,(75, 60),1), BadTile(11,(65, 60),1), EventTile(12,(55, 60),1), BadTile(13,(45, 60),1), EventTile(14,(35,60),1), #route 1
                    StopTile(15, (25, 60), stop_events[1]),GoodTile(16, (30, 75)), BadTile(17, (40, 75)), EventTile(18, (50, 75)), StopTile(19,(60, 75), stop_events[2]), 
                    EventTile(20,(70, 85)),
                ]
        return boardClass.Board(tiles)

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

