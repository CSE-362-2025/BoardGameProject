"""
Authors: Bottom Six
Created: 2025/02/14
Last Edited: 2025/02/17
Board Class sets up the board and helps determine the tile type the player is on.
"""
import pygame
import player


class Board:
    
    def __init__(self, tiles, size):

        self.tiles = tiles
        self.size = size

    # returns tile at position
    def get_tile(self, position):
        pass

    # returns a list of positions of the players [<player, position>]
    def get_player_positions(self, players):
        pass
