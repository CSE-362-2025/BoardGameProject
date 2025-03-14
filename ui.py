import pygame
import random

# Constants
WINDOW_SIZE_X = 1080
WINDOW_SIZE_Y= 720
BG_COLOR = (30, 30, 30)  # Dark gray background
FONT_COLOR = (255, 255, 255)  # White text

DICE_SIZE = 80
DICE_POS = (225, 400)  # Adjust this based on your UI layout
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TURN_SIZE = 80
TURN_POS = (100, 400)  # Adjust this based on your UI layout


class UI():

    # player is current player, changes during switch_turn()
    def __init__(self, game_manager=None, player=None):
        self.game_manager = game_manager
        self.player = player
        self.screen = pygame.display.set_mode((WINDOW_SIZE_X, WINDOW_SIZE_Y), pygame.RESIZABLE)
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


    def display_board(self, board, players):
        self.screen.fill(BG_COLOR)  # Clear screen
        board.draw(self.screen, players)
        pygame.display.flip()  # Update display

    def display_stats(self):
        # Example of displaying player stats in the top-right corner
        self.font = pygame.font.Font(None, 16)
        if self.player:
            stats_text = f"{self.player.name}'s Stats: {self.player.stats}"  # You can customize this to show actual stats
            stats_surface = self.font.render(stats_text, True, FONT_COLOR)
            stats_rect = stats_surface.get_rect(topright=(self.screen.get_width() - 10, 10))
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


    def roll_dice(self):
        self.dice_value = random.randint(1, 6)  # Roll dice
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

    def display_computer_decision(self, event, choice_idx):
        # Display the result of the computer's decision
        self.display_message(f"Computer chose: {event.choices[choice_idx].name}")
    
    def display_non_decision_event(self, event):
        # Display the non-decision event
        self.display_message(f"{event.name}: {event.description}")
        self.game_manager.accept_event(event)

    def display_computer_non_decision_event(self, event):
        # Display the result of the computer's non-decision event
        self.display_message(f"Computer: {event.name} | Result: {event.result}")
        self.game_manager.accept_event(event)

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
