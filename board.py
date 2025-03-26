"""
Authors: Bottom Six
Created: 2025/02/14
Last Edited: 2025/03/18
Board Class sets up the board and helps determine the tile type the player is on.
"""
import pygame
import player

FONT_COLOR = (255, 255, 255)  # White text

class Board:
    
    def __init__(self, tiles, year):
        self.tiles = tiles
        self.size = len(tiles)
        self.year = year

    # returns tile at position
    def get_tile(self, position):
        return self.tiles[position]

    # returns a list of positions of the players [<player, position>]
    def get_player_positions(self, players):
        pass

    def draw(self, screen, players):
        screen_width = screen.get_width()/100
        screen_height = screen.get_height()/100
        font = pygame.font.Font(None, 16)
        # Draw tiles
        TILE_SIZE = (screen_width*8, screen_height*8)
        mid = (TILE_SIZE[0]/2, TILE_SIZE[1]/2)
        for tile in self.tiles:
            position = tile.get_screen_pos()
            # Draw tile rectangle
            rect = pygame.Rect((position[0])*screen_width-mid[0], (position[1])*screen_height-mid[1], TILE_SIZE[0], TILE_SIZE[1])
            pygame.draw.rect(screen, tile.get_colour(), rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 2)  # Black border

            # Draw tile type letter in center
            text_surface = font.render(tile.get_type()[:], True, FONT_COLOR)
            text_rect = text_surface.get_rect(center=rect.center)
            screen.blit(text_surface, text_rect)

        # Draw players
        for player in players:
            try:
                position = self.tiles[(player.position)].get_screen_pos()
            except Exception as e:
                position = self.tiles[-1].get_screen_pos()
            position = (position[0], position[1], mid)
            player.draw(screen, position)

