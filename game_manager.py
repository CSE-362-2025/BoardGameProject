"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Manages the game and tracks when each event should occur
"""
import pygame
import board
import event
import ui


class GameManager:

    def __init__(self, board, players, events, ui, game_database):
        
        self.board = board
        self.players = players
        self.events = events
        self.ui = ui
        self.game_database = game_database

        self.turn_count = 0

    # plays all logic for playing human turn
    def play_turn(self):
        pass

    def play_computer_turn(self):
        pass

    def start_game(self):
        pass

    def end_game(self):
        pass

    def switch_turn(self):
        pass

    def roll_dice(self):
        pass

    def event_choice(self, event, choice_idx):
        pass

    def accept_event(self, event):
        pass

    def get_random_event(self):
        pass

    def is_game_over(self):
        pass

    def generate_good_tile_effects(self):
        pass

    def generate_bad_tile_effects(self):
        pass

