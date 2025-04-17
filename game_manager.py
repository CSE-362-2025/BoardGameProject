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
from statistics import mean
from llm_model import llm
from database import GameDatabase


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

        self.has_gpu = False

    # plays all logic for playing human turn
    def play_turn(self, dice_value):

        self.current_player.has_moved = True

        roll = dice_value
        self.current_player.rolls.append(roll)  # appends the roll to player list

        print(f"Player {self.current_player.name} rolled {roll}")

        if self.current_player.branch:
            self.current_player.branch = False
            self.current_player.position = self.current_player.next_pos
            self.current_player.on_alt_path = True

        print(
            f"{self.current_player.name}'s position before move {self.current_player.position}"
        )

        # Checking if hitting a stop tile
        for i in range(
            self.current_player.position + 1, self.current_player.position + roll + 1
        ):
            tile = self.board.get_tile(i)
            if not tile:
                tile = self.board.get_tile(i - 100)
                if not tile:
                    print("OUT OF BOUNDS WHEN LOOKING FOR A STOPTILE")
                    break

            if tile.get_type() == "StopTile":
                print("Found StopTile")
                steps = tile.position - self.current_player.position
                self.current_player.move(steps)
                print(
                    f"{self.current_player.name}'s' Position after move: {self.current_player.position}"
                )
                print(f"Landed on StopTile")
                if len(tile.paths) > 1:
                    self.current_player.branch = True

                self.ui.display_decision_event(tile.event)
                return  # Exit after stop tile processing

        # Move the player if not a stop tile
        self.current_player.move(roll)

        print(
            f"{self.current_player.name}'s Position after move: {self.current_player.position}"
        )

        tile = self.board.get_tile(self.current_player.position)

        if not tile and self.current_player.on_alt_path:
            self.current_player.on_alt_path = False
            self.current_player.position -= 100  # Puts the position back on "main" path
            tile = self.board.get_tile(self.current_player.position)
            # print(tile.position, self.current_player.position)

        if not tile:
            self.current_player.position = self.board.size
            tile = self.board.tiles[len(self.board.tiles) - 1]

        if tile.get_type() == "EndTile":
            print(f"{self.current_player.name} is at the end of the board")
            self.current_player.at_end = True
            self.ui.display_end_event(["You have reached the end of the board"])

            if self.is_game_over():
                self.end_game()

            return

        self.current_player.tile_counts[tile.get_type()] += 1

        # Handle events based on tile type
        if tile.get_type() == "EventTile":
            event = self.get_random_event()
            self.ui.display_decision_event(event)

        elif tile.get_type() in ["GoodTile", "BadTile"]:
            effects = (
                self.generate_good_tile_effects()
                if tile.get_type() == "GoodTile"
                else self.generate_bad_tile_effects()
            )
            self.current_player.change_stats(effects[1])
            # self.ui.display_message(f"{effects[0]}")
            self.ui.display_non_decision_event(effects)

        else:
            print(tile.get_type())
            raise Exception("Invalid tile type")

        print(f"Landed on {tile.get_type()}")

    def play_computer_turn(self):
        pass

    def start_game(self, is_new_game=True):
        db = GameDatabase()
        db.connect("")
        print("Starting")
        events = self.get_events(0)
        self.events = events
        self.board = self.get_board(0)
        self.players = self.get_players()

        if is_new_game:
            self.current_player = self.players[0]
        else:
            self.current_player = db.get_curr_player(game_manager=self)
        print(self.current_player)
        self.ui.change_current_player(self.current_player)
        db.close_connection()
        return is_new_game

    def get_events(self, year):
        # Create events
        with open("game_objects/events.json") as file:
            events_raw = json.load(file)

        events = []
        for event in events_raw:
            events.append(
                Event(
                    event["name"],
                    event["description"],
                    event["choices"],
                    rarity=event["rarity"],
                    phase=event["phase"],
                )
            )
        return events

    def get_board(self, year):
        boards = []
        with open("game_objects/boards.json") as file:
            boards_raw = json.load(file)

        board_raw = boards_raw[0]
        tiles = []
        for tile in board_raw["tiles"]:
            if tile["tile_type"] == "StopTile":
                event_raw = tile["event"]
                if event_raw:
                    if event_raw["branch"]:
                        event = Event(
                            event_raw["name"],
                            event_raw["description"],
                            event_raw["choices"],
                            branch=event_raw["branch"],
                        )
                    else:
                        event = Event(
                            event_raw["name"],
                            event_raw["description"],
                            event_raw["choices"],
                        )
                else:
                    event = None

                if event_raw["branch"]:
                    tiles.append(
                        StopTile(
                            tile["position"],
                            tile["screen_position"],
                            event,
                            tile["paths"],
                        )
                    )
                else:
                    tiles.append(
                        StopTile(tile["position"], tile["screen_position"], event, [])
                    )
            else:
                tiles.append(
                    Tile(tile["position"], tile["screen_position"], tile["tile_type"])
                )

        boards.append(Board(tiles, board_raw["year"]))
        board = boards[0]
        return board

    def get_players(self):

        # Create players
        players = [
            Player(
                "Bruno",
                (50, 200, 50),
                image="Resources/Pawn_Blue.png",
                portrait="Resources/Portrait_Blue.png",
                next_up="Resources/Next_Blue.png",
            ),
            Player(
                "Charlie",
                (50, 200, 200),
                image="Resources/Pawn_Yellow.png",
                portrait="Resources/Portrait_Yellow.png",
                next_up="Resources/Next_Yellow.png",
            ),
            Player(
                "Dani",
                (200, 200, 200),
                image="Resources/Pawn_Green.png",
                portrait="Resources/Portrait_Green.png",
                next_up="Resources/Next_Green.png",
            ),
            Player(
                "Alex",
                (200, 200, 50),
                image="Resources/Pawn_Red.png",
                portrait="Resources/Portrait_Red.png",
                next_up="Resources/Next_Red.png",
            ),
        ]
        return players

    def end_game(self):
        print("THE GAME IS OVER")

        self.generate_awards()
        self.generate_end_text()
        if self.has_gpu:
            self.ai_summary()
        for player in self.players:
            # print(f"{player.name} stats: {player.stats}")
            # print(f"{player.name} awards: {player.awards}")
            # print(f"{player.name} end text: {player.end_text}")
            if self.has_gpu:
                print(f"{player.name} ai summary: {player.ai_summary}")

    #  gives awards to players with the highest stats
    def generate_awards(self):

        stats = ["academic", "bilingual", "military", "athletic", "social"]

        # returns a list of the player objects with the max for that stat
        def max_player_stat(players, stat):

            max_players = []

            max_player = players[0]
            for player in players[1:]:
                if player.stats[stat] > max_player.stats[stat]:
                    max_player = player

            max_players.append(max_player)

            for player in players:
                if max_player.name == player.name:
                    continue

                elif max_player.stats[stat] == player.stats[stat]:
                    max_players.append(player)

            return max_players

        for stat in stats:
            max_players = max_player_stat(self.players, stat)

            for player in max_players:
                player.awards[stat] = True


    #  writes an endgame summary to player object in player.end_text
    def generate_end_text(self):

        idx = random.randint(0, len(self.players)-1)
        player = self.players[idx]

        player.end_text = f"You rolled an average of {mean(player.rolls):.1f}. Nice!"

        idx = (idx + 1) % len(self.players)
        player = self.players[idx]

        player.end_text = f"You landed on {player.tile_counts['BadTile']} BadTiles and {player.tile_counts['GoodTile']} GoodTiles. Wow!"

        idx = (idx + 1) % len(self.players)
        player = self.players[idx]

        player.end_text = f"You rolled {player.rolls.count(1)} 1s and {player.rolls.count(6)} 6s. Interesting!"

        idx = (idx + 1) % len(self.players)
        player = self.players[idx]

        player.end_text = f"You landed on {player.tile_counts['EventTile']} EventTiles. Cool!"



    # Uses a Large Language Model to write a summary about events played for each player
    def ai_summary(self):

        for player in self.players:

            # check if player already has ai_summary generated
            if len(player.ai_summary) > 0:
                continue

            prompt = f"""
            You are a machine which generates a summary and detailed story of {player.name}'s journey through a Royal Military College board game.
            You will only get the names of the events played in the ordered they were played by the player throughout the game and the choice the player made.
            Contain generated summary between a START and END token.
            Events played and choice:

            """

            for event in player.events_played:
                prompt = (
                    prompt
                    + f"Event name: {event[0]} and {player.name} chose: {event[1]} \n"
                )

            prompt = prompt + "\n generate summary: START"

            summary = llm(prompt)

            player.ai_summary = summary

    def switch_turn(self):
        self.turn_count += 1
        self.current_player = self.players[(self.turn_count) % len(self.players)]

        i = 0
        if self.current_player.at_end:
            while i < 4:
                self.current_player = self.players[
                    (self.turn_count + i) % len(self.players)
                ]

                if self.current_player.at_end:
                    i += 1
                else:
                    break

        if i == 4:
            self.end_game()
            return

        self.ui.change_current_player(self.current_player)
        self.ui.update()
        # print(self.current_player.name)

    def roll_dice(self):
        return random.randint(1, 6)

    # used by the UI after human picks event choice
    def event_choice(self, event, choice_idx):
        event.apply_result(self.current_player, choice_idx)
        print(f"Player's choice {choice_idx}")

        if event.branch:
            pos = self.current_player.position
            self.current_player.next_pos = (
                self.board.get_tile(pos).paths[choice_idx - 1]
            ) - 1
            print(f"Current Player Next Pos: {self.current_player.next_pos}")

        self.current_player.store_event(
            event, choice_idx
        )  # store event in player's history
        self.ui.display_board(self.board, self.players)

    # gets a random event from the list of events that
    # meets the criteria of the player's stats, must take into account rarity
    def get_random_event(self):
        number = random.randint(1, 20)
        i = 0  # avoid infinate loop

        # common 75%
        if number >= 1 and number <= 15:
            while i < 500:
                event = random.choice(self.events)
                if not (
                    event.rarity == 0
                    and self.board.year in event.phase
                    and event.id in self.current_player.events_played
                ):
                    i += 1
                    continue
                else:
                    break

        # rare 20%
        elif number >= 16 and number <= 19:
            while i < 500:
                event = random.choice(self.events)
                if (
                    event.rarity == 1
                    and self.board.year in event.phase
                    and event.id in self.current_player.events_played
                ):
                    i += 1
                    continue
                else:
                    break

        # super rare 5%
        else:
            while i < 500:
                event = random.choice(self.events)
                if (
                    event.rarity == 2
                    and self.board.year in event.phase
                    and event.id in self.current_player.events_played
                ):
                    i += 1
                    continue
                else:
                    break

        # adding return statement
        return event

    # Return true if the entire game is over
    def is_game_over(self):
        if self.players:
            for player in self.players:
                if player.at_end:
                    continue
                else:
                    return False

            return True
        else:
            return False

    # returns a message and stat changes in a tuple
    def generate_good_tile_effects(self):

        number = random.randint(1, 5)

        if number == 1:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You took extra french lessons! (+1 Biligual)",
                    {
                        "bilingual": 1,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]
            elif number == 2:
                return [
                    "You spoke to someone in your second language! (+1 Biligual)",
                    {
                        "bilingual": 1,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]
            else:
                return [
                    "You wrote a bilingual email! (+1 Biligual)",
                    {
                        "bilingual": 1,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

        elif number == 2:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You ran a 5k! (+1 Athletic)",
                    {
                        "bilingual": 0,
                        "athletic": 1,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    "You did a workout! (+1 Athletic)",
                    {
                        "bilingual": 0,
                        "athletic": 1,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You went to gym class! (+1 Athletic)",
                    {
                        "bilingual": 0,
                        "athletic": 1,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

        elif number == 3:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You did well on a test! (+1 Academic)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 1,
                        "military": 0,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    "You completed a project for class! (+1 Academic)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 1,
                        "military": 0,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You did a presentation for school! (+1 Academic)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 1,
                        "military": 0,
                        "social": 0,
                    },
                ]

        elif number == 4:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You did a drill practice! (+1 Military)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 1,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    "You had an inspection this morning! (+1 Military)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 1,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You polished your oxfords! (+1 Military)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 1,
                        "social": 0,
                    },
                ]

        else:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You answered a question correctly in class! (+1 Social)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 1,
                    },
                ]

            elif number == 2:
                return [
                    "You went to the mess! (+1 Social)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 1,
                    },
                ]

            else:
                return [
                    "You hung out with friends! (+1 Social)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 1,
                    },
                ]

    def generate_bad_tile_effects(self):

        number = random.randint(1, 5)

        if number == 1:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You forgot your french homework! (-1 Bilingual)",
                    {
                        "bilingual": -1,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    'You said "je suis fini" instead of "j\'ai fini" and all the francos laughed at you! (-1 Bilingual)',
                    {
                        "bilingual": -1,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You failed your french test! (-1 Bilingual)",
                    {
                        "bilingual": -1,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

        elif number == 2:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You failed the PPT Run! (-1 Athletic)",
                    {
                        "bilingual": 0,
                        "athletic": -1,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    "You got dunked on in gym class! (-1 Athletic)",
                    {
                        "bilingual": 0,
                        "athletic": -1,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You lost every intramural game this season! (-1 Athletic)",
                    {
                        "bilingual": 0,
                        "athletic": -1,
                        "academic": 0,
                        "military": 0,
                        "social": 0,
                    },
                ]

        elif number == 3:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You got a 2/20 on your math quiz. Yikes! (-1 Academic)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": -1,
                        "military": 0,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    "You failed PSE103. Nobody even thought that was possible! (-1 Academic)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": -1,
                        "military": 0,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You got a 0 on your history proposal. Better cite some better sources! (-1 Academic)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": -1,
                        "military": 0,
                        "social": 0,
                    },
                ]

        elif number == 4:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You forgot to polish your oxfords and got called out by the duty officer! (-1 Military)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": -1,
                        "social": 0,
                    },
                ]

            elif number == 2:
                return [
                    "You forgot to salute an officer! (-1 Military)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": -1,
                        "social": 0,
                    },
                ]

            else:
                return [
                    "You turned the wrong way doing drill! (-1 Military)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": -1,
                        "social": 0,
                    },
                ]

        else:
            number = random.randint(1, 3)

            if number == 1:
                return [
                    "You dropped your tray in the CDH and food went everywhere! (-1 Social)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": -1,
                    },
                ]

            elif number == 2:
                return [
                    "You just realise that you haven't spoken to another human in over a week! (-1 Social)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": -1,
                    },
                ]

            else:
                return [
                    "You said something dumb in class and everyone laughed! (-1 Social)",
                    {
                        "bilingual": 0,
                        "athletic": 0,
                        "academic": 0,
                        "military": 0,
                        "social": -1,
                    },
                ]

    def save_state(self):
        db = GameDatabase()
        db.connect("")
        db.save_game(self)
        db.close_connection()

    def load_state(self) -> bool:
        db = GameDatabase()
        db.connect("")
        ret = db.load_game(self)
        db.close_connection()
        return ret