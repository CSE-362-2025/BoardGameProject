import pygame
import random

# Constants
TILE_SIZE = 100  # Size of each square
GRID_SIZE = 5  # Assuming a 6x6 board
WINDOW_SIZE = TILE_SIZE * GRID_SIZE
BG_COLOR = (30, 30, 30)  # Dark gray background
FONT_COLOR = (255, 255, 255)  # White text
PLAYER_RADIUS = 20  # Radius of player circle

DICE_SIZE = 80
DICE_POS = (225, 400)  # Adjust this based on your UI layout
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TURN_SIZE = 80
TURN_POS = (100, 400)  # Adjust this based on your UI layout


# Colors for different tile types
TILE_COLORS = {
    "Good": (50, 200, 50),  # Green
    "Bad": (200, 50, 50),  # Red
    "Event": (50, 50, 200),  # Blue
    "Stop": (200, 200, 50)  # Yellow
}

class UI():

    # player is current player, changes during switch_turn()
    def __init__(self, game_manager=None, player=None):
        self.game_manager = game_manager
        self.player = player
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        self.font = pygame.font.Font(None, 16)
        self.dice_value = 0

        self.message = None  # Variable to store the current message
        self.message_duration = 0  # Number of frames the message will stay on screen

    def update(self, board, players):
        """Updates and draws all necessary UI components."""
        # Draw the board, dice, and stats
        self.screen.fill((0, 0, 0))  # Clear the screen first
        self.display_board(board, players)  # Call a method to draw the game board (implement as needed)
        self.display_dice()   # Call a method to display the dice
        self.display_stats()  # Call a method to display player stats, if any
        self.display_current_turn()
        self.display_turn()

        # If there's a message to display, show it
        if self.message_duration > 0:
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomleft=(25, 500))
            self.screen.blit(text_surface, text_rect)
            self.message_duration -= 1

        pygame.display.flip()  # Update the display

    # This will have to be completely redone
    def display_board(self, board, players):
        self.screen.fill(BG_COLOR)  # Clear screen

        # Draw tiles
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile_index = i * GRID_SIZE + j
                if tile_index < len(board.tiles):
                    tile = board.tiles[tile_index]  # Get tile object
                    tile_color = TILE_COLORS.get(tile.get_type(), (100, 100, 100))  # Default gray if unknown
                    
                    # Draw tile rectangle
                    rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(self.screen, tile_color, rect)
                    pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Black border

                    # Draw tile type letter in center
                    text_surface = self.font.render(f"{tile.get_type()[:]} {tile.position}", True, FONT_COLOR)
                    text_rect = text_surface.get_rect(center=rect.center)
                    self.screen.blit(text_surface, text_rect)

        # Draw players
        for player in players:
            player_x = (player.position % GRID_SIZE) * TILE_SIZE + TILE_SIZE // 2
            player_y = (player.position // GRID_SIZE) * TILE_SIZE + TILE_SIZE // 2
            
            pygame.draw.circle(self.screen, player.color, (player_x-25, player_y-25), PLAYER_RADIUS)

            # Draw player name or symbol above the circle
            player_text = self.font.render(player.name[-1], True, FONT_COLOR)
            player_text_rect = player_text.get_rect(center=(player_x-25, player_y - PLAYER_RADIUS - 25))
            self.screen.blit(player_text, player_text_rect)

        pygame.display.flip()  # Update display

    def display_stats(self):
        # Example of displaying player stats in the top-right corner
        self.font = pygame.font.Font(None, 16)
        if self.player:
            stats_text = f"{self.player.name}'s Stats: {self.player.stats}"  # You can customize this to show actual stats
            stats_surface = self.font.render(stats_text, True, FONT_COLOR)
            stats_rect = stats_surface.get_rect(topright=(WINDOW_SIZE - 10, 10))
            self.screen.blit(stats_surface, stats_rect)
            pygame.display.flip()

    def display_dice(self):
        # Draw dice background (square)
        dice_rect = pygame.Rect(DICE_POS[0], DICE_POS[1], DICE_SIZE, DICE_SIZE)
        pygame.draw.rect(self.screen, WHITE, dice_rect)  # Background of the dice
        pygame.draw.rect(self.screen, BLACK, dice_rect, 3)  # Border for the dice

        # Draw dice value (centered in the dice square)
        text_surface = self.font.render(str(self.dice_value), True, BLACK)
        text_rect = text_surface.get_rect(center=dice_rect.center)  # Center the text inside the dice square
        self.screen.blit(text_surface, text_rect)  # Draw the text on the screen

        # Update the display to reflect changes
        pygame.display.update()  # Update display after drawing the dice


    def display_turn(self):
        turn_rect = pygame.Rect(TURN_POS[0], TURN_POS[1], TURN_SIZE, TURN_SIZE)
        pygame.draw.rect(self.screen, WHITE, turn_rect)  # 
        pygame.draw.rect(self.screen, BLACK, turn_rect, 3)  # 

        text_surface = self.font.render("Next Turn", True, BLACK)
        text_rect = text_surface.get_rect(center=turn_rect.center)  # Center the text inside the dice square
        self.screen.blit(text_surface, text_rect)  # Draw the text on the screen
        
        pygame.display.update()  # Update display

    # Rolling 1 only for testing
    def roll_dice(self):
        self.dice_value = random.randint(1, 1)  # Roll dice
        self.display_dice()  # Update display after rolling
        self.game_manager.play_turn(self.dice_value)

    def handle_click(self, pos):
        # Check if the click was inside the dice area
        dice_rect = pygame.Rect(DICE_POS[0], DICE_POS[1], DICE_SIZE, DICE_SIZE)
        if dice_rect.collidepoint(pos):
            self.roll_dice()

        turn_rect = pygame.Rect(TURN_POS[0], TURN_POS[1], TURN_SIZE, TURN_SIZE)
        if turn_rect.collidepoint(pos):
            self.game_manager.switch_turn()

    # Pass in event and display decision choices
    def display_decision_event(self, event):
        self.display_message(f"{event.name}: {', '.join([choice['text'] for choice in event.choices])}")
        choice_idx = random.randint(1, len(event.choices))
        print(f"Chose: {choice_idx}")
        self.game_manager.event_choice(event, choice_idx)

    def display_stoptile_event(self, event):
        self.display_message(f"{event.name}: {', '.join([choice['text'] for choice in event.choices])}")
        choice_idx = 2
        # choice_idx = random.randint(1, len(event.choices))
        print(f"Chose: {choice_idx}, {event.choices[choice_idx-1]['text']}")
        self.game_manager.branching_event_choice(event, choice_idx)

    def display_computer_decision(self, event, choice_idx):
        # Display the result of the computer's decision
        self.display_message(f"Computer chose: {event.choices[choice_idx].name}")

    # Display game messages such as player turn, etc.
    def display_message(self, message, duration=200):
        # Set background color for the message area (optional)
        self.message = message
        self.message_duration = duration

    def display_current_turn(self):
        # Example of displaying player stats in the top-right corner
        self.font = pygame.font.Font(None, 16)
        if self.player:
            stats_text = f"{self.player.name}'s Turn"  # 
            stats_surface = self.font.render(stats_text, True, FONT_COLOR)
            stats_rect = stats_surface.get_rect(bottomright=(450, 450))
            self.screen.blit(stats_surface, stats_rect)
            pygame.display.flip()

    def change_current_player(self, player):
        self.player = player
        # self.display_message(f"{player.name}'s turn")

    def display_roll(self, roll):
        # Display the roll value
        self.display_message(f"Rolled: {roll}")
