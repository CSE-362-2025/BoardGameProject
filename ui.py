"""
Authors: Bottom Six
Last Edit: 2025/02/17
Keeps track of the user interfact and runs event dependant on the results
"""
import pygame 
import random

# Constants
TILE_SIZE = 80  # Size of each square
GRID_SIZE = 6  # Assuming a 6x6 board
WINDOW_SIZE = TILE_SIZE * GRID_SIZE
BG_COLOR = (30, 30, 30)  # Dark gray background
FONT_COLOR = (255, 255, 255)  # White text

# Colors for different tile types
TILE_COLORS = {
    "Good": (50, 200, 50),  # Green
    "Bad": (200, 50, 50),  # Red
    "Event": (50, 50, 200),  # Blue
    "Stop": (200, 200, 50)  # Yellow
}

class UI():

    # player is current player, changes during switch_turn()
    def __init__(self, game_manager, player=None):
        self.game_manager = game_manager
        self.player = player
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.font = pygame.font.Font(None, 36)

    def display_board(self, board, players):
        self.screen.fill(BG_COLOR)  # Clear screen

        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = board.tiles[i * GRID_SIZE + j]  # Get tile object
                tile_color = TILE_COLORS.get(tile.get_type(), (100, 100, 100))  # Default gray if unknown
                
                # Draw tile rectangle
                rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, tile_color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Black border

                # Draw tile type letter in center
                text_surface = self.font.render(tile.get_type()[0], True, FONT_COLOR)
                text_rect = text_surface.get_rect(center=rect.center)
                self.screen.blit(text_surface, text_rect)

        pygame.display.flip()  # Update display

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

    def display_roll(self, roll):
        pass
