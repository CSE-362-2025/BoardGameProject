import pygame
from game_manager import GameManager
from board import Board
from player import Player
from ui import UI
from event import Event, DecisionEvent, StaticEvent
from tiles import GoodTile, BadTile, EventTile, StopTile
import json

# Constants
SCREEN_WIDTH = 2000
SCREEN_HEIGHT = 2000

def main():
    # Initialize pygame
    pygame.init()
    
    # Set up display
    pygame.display.set_caption("Board Game")

    # Create UI instance
    ui = UI()

    # Create events
    
    with open("game_objects/events.json") as file:
        events_raw = json.load(file)
    
    events = []
    for event in events_raw:
        if event['type'] == "Decision":
            events.append(DecisionEvent(event['name'], event['description'], 
                                        event['criteria'], event['choices'],
                                        event['rarity']))

        elif event['type'] == "Static":
            events.append(StaticEvent(event['name'], event['description'], 
                                        event['criteria'], event['result'],
                                        event['rarity']))
            
    event_stoptile = StaticEvent("StopTile Event", "...", None, None, 0)
    print(event_stoptile.get_type())


    # Create board with tiles
    tiles = [
        GoodTile(0), BadTile(1), GoodTile(2), BadTile(3), EventTile(4),
        GoodTile(5), BadTile(6), GoodTile(7), BadTile(8), EventTile(9),
        GoodTile(10), BadTile(11), GoodTile(12), BadTile(13), StopTile(14, event_stoptile),
        GoodTile(15), BadTile(16), GoodTile(17), BadTile(18), EventTile(19),
        
    ]
    board = Board(tiles)

    # Create players
    players = [
        Player("Player 1", (50, 200, 50), {"bilingual": 5, "athletic": 5, "academic": 5, "military": 5, "social": 5}),
        Player("Player 2", (50, 200, 200), {"bilingual": 5, "athletic": 5, "academic": 5, "military": 5, "social": 5}),
        Player("Player 3", (200, 200, 200), {"bilingual": 5, "athletic": 5, "academic": 5, "military": 5, "social": 5}),
        Player("Player 4", (200, 200, 50), {"bilingual": 5, "athletic": 5, "academic": 5, "military": 5, "social": 5}),

    ]


    # Initialize GameManager
    game_manager = GameManager(board, players, events, ui, game_database=None)
    game_manager.start_game()

    ui.game_manager = game_manager

    clock = pygame.time.Clock()
    ui.update(board, players)


    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop when the user closes the window
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui.handle_click(event.pos)  # Check if dice was clicked

        # Display the current state
        # ui.update(board, players)

        # Check if the game is over
        if game_manager.is_game_over():
            ui.display_message("Game Over!")  # Display game over message
            pygame.display.update()  # Ensure the last message is displayed
            pygame.time.wait(2000)  # Wait for a couple of seconds before quitting
            running = False

        # Display the current state
        if game_manager.current_player.has_moved:
            ui.update(board, players)
            game_manager.current_player.has_moved = False

        # Update the screen (can be flipped to update only parts of the screen)
        pygame.display.flip()  # Update the entire screen
        clock.tick(60)

    pygame.quit()  # Quit the game and close the window


if __name__ == "__main__":
    main()
