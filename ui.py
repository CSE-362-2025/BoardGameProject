"""
Authors: Bottom Six
Last Edit: 2025/02/17
Keeps track of the user interfact and runs event dependant on the results
"""
import pygame 
import random


class UI():

    def __init__(self, game_manager, player=None):
        self.game_manager = game_manager
        self.player = player

    def display_board():
        pass

    def display_stats():
        pass

    # Pass in event and display
    def display_event(event):
        pass

    # Prompt the user to make a choice, returns int of index of choice
    def prompt_choice():
        pass

    # Display game messages such as player turn, ect
    def display_message():
        pass
