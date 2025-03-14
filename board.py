"""
Authors: Bottom Six
Created: 2025/02/14
Last Edited: 2025/02/17
Board Class sets up the board and helps determine the tile type the player is on.
"""
import pygame
import player

class Board:
    
    def __init__(self, tiles):

        self.tiles = tiles
        self.size = len(tiles)

    # returns tile at position
    def get_tile(self, position):
        return self.tiles[position]

    # returns a list of positions of the players [<player, position>]
    def get_player_positions(self, players):
        pass


     
