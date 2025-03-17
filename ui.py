import pygame
import random

# Constants
WINDOW_SIZE_X = 1080
WINDOW_SIZE_Y= 720
BG_COLOR = (30, 30, 30)  # Dark gray background
FONT_COLOR = (255, 255, 255)  # White text

BUTTON_SIZE = 80 
# Adjust this based on your UI layout (percentage based)
DICE_POS = (60, 100) 
NEXT_POS = (40,100)
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
        self.Buttons = [Buttons(DICE_POS, (BUTTON_SIZE,BUTTON_SIZE), "Dice"), Buttons(NEXT_POS, (BUTTON_SIZE,BUTTON_SIZE), "Next Turn")]
        self.buttonevents = []
        self.dice_value = 0
        self.message = None  # Variable to store the current message
        self.message_duration = 0  # Number of frames the message will stay on screen

    def update(self, board, players):
        """Updates and draws all necessary UI components."""  
        # Draw the board, dice, and stats
        self.screen.fill((0, 0, 0))  # Clear the screen first
        self.display_board(board, players)  # Call a method to draw the game board (implement as needed)
        self.display_buttons()   # Call a method to display the dice
        self.display_stats()  # Call a method to display player stats, if any
        self.display_current_turn()

        # If there's a message to display, show it
        if self.message_duration > 0:
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomleft=(25, 500))
            self.screen.blit(text_surface, text_rect)
            self.message_duration -= 1


    def display_board(self, board, players):
        self.screen.fill(BG_COLOR)  # Clear screen
        board.draw(self.screen, players)

    def display_stats(self):
        # Example of displaying player stats in the top-right corner
        self.font = pygame.font.Font(None, 16)
        if self.player:
            stats_text = f"{self.player.name}'s Stats: {self.player.stats}"  # You can customize this to show actual stats
            stats_surface = self.font.render(stats_text, True, FONT_COLOR)
            stats_rect = stats_surface.get_rect(topright=(self.screen.get_width() - 10, 10))
            self.screen.blit(stats_surface, stats_rect)

    def roll_dice(self):
        self.dice_value = random.randint(1, 6)  # Roll dice
        self.display_dice()  # Update display after rolling
        self.game_manager.play_turn(self.dice_value)

    def display_buttons(self):
        for button in self.Buttons:
            if button.visible:
                button.display(self.screen)

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

    def change_current_player(self, player):
        self.player = player
        # self.display_message(f"{player.name}'s turn")

    def display_roll(self, roll):
        # Display the roll value
        self.display_message(f"Rolled: {roll}")

    def handle_click(self, pos):
        for button in self.Buttons:
            if button.visible:
                result = button.handle_click(self.screen, pos)
                if result:
                    self.buttonevents.append(result)

    def run(self):
        """React to events in the list FIFO, and remove all following copies of that event"""
        if len(self.buttonevents) > 0:
            next = self.buttonevents[0]
            self.buttonevents = list_edit(self.buttonevents, next)
            match next:
                case 'Dice':
                    self.roll_dice()
                case 'Next Turn':
                    self.change_current_player(self.player)
            


def list_edit(list, item):
    """Removes all copies of an element from a list"""
    list = [i for i in list if i != item]
    return list






class Buttons:
    """Creates a button that can track itself visually and its events"""
    def __init__(self, centre, size, type):
        self.visible = True
        self.position = centre
        self.size = size
        self.type = type

    def turn_on(self):
        self.visible = True
    
    def turn_off(self):
        self.visible = False

    def display(self, screen):
        screen_width = screen.get_width()/100
        screen_height = screen.get_height()/100
        font = pygame.font.Font(None, 16)
        # Draw dice background (square)
        button_rect = pygame.Rect((self.position[0])*screen_width-self.size[0]/2,(self.position[1])*screen_height-self.size[1], self.size[0], self.size[1])
        pygame.draw.rect(screen, WHITE, button_rect)  # Background of the dice
        pygame.draw.rect(screen, BLACK, button_rect, 3)  # Border for the dice

        # Draw dice value (centered in the dice square)
        text_surface = font.render(str(self.type), True, BLACK)
        text_rect = text_surface.get_rect(center=button_rect.center)  # Center the text inside the dice square
        screen.blit(text_surface, text_rect)  # Draw the text on the screen

    def handle_click(self, screen, pos):
        screen_width = screen.get_width()/100
        screen_height = screen.get_height()/100
        font = pygame.font.Font(None, 16)
        # Check if the click was inside the dice area
        button_rect = pygame.Rect((self.position[0])*screen_width-self.size[0]/2,(self.position[1])*screen_height-self.size[1], self.size[0], self.size[1])
        if button_rect.collidepoint(pos):
            return self.type
