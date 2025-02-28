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
    def __init__(self, board, players):
        
        self.board = board
        self.players = players

        self.turn_count = 0

    def start_game(self):
        pass

    def end_game(self):
        pass

    def switch_turn(self):
        pass

    def roll_dice(self):
        pass

    def is_game_over(self):
        pass

