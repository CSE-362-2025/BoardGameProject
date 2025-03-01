"""
Authors: Bottom Six
Last Edit: 2025/02/17
Keeps track of the user interfact and runs event dependant on the results
"""
import pygame 
import random


class UI():

    # player is current player, changes during switch_turn()
    def __init__(self, game_manager, player=None):
        self.game_manager = game_manager
        self.player = player

    def display_board(self):
        pass

    def display_stats(self):
        pass

    def display_dice(self):
        pass

    # Pass in event and display
    def display_decision_event(self, event):
        pass

    def display_computer_decision(self, event, choice_idx):
        pass

    def display_non_decision_event(self, event):
        pass

    def display_computer_non_decision_event(self, event):
        pass

    # Display game messages such as player turn, ect
    def display_message(self, message):
        pass

    def change_current_player(self, player):
        pass
