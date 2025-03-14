import pygame
from game_manager import GameManager
from board import Board
from player import Player
from ui import UI
from event import DecisionEvent, StaticEvent
from tiles import GoodTile, BadTile, EventTile, StopTile
import json


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
            
    event_stoptile_1 = StaticEvent("StopTile 1", "PPT! (+2 Athletic)", None, {
                "bilingual": 0,
                "athletic": 2,
                "military": 0,
                "academic": 0,
                "social": 0,
            }, 0)
    event_stoptile_2 = StaticEvent("StopTile 2", "Exams! (+3 Academic)", None, {
                "bilingual": 0,
                "athletic": 0,
                "military": 0,
                "academic": 3,
                "social": 0,
            }, 0)

    # Create board with tiles
    tiles = [
        GoodTile((5, 5)), BadTile((10, 10)), GoodTile((15, 15)), BadTile((20, 20)), EventTile((25, 25)),
        GoodTile((30, 30)), BadTile((35, 35)), GoodTile((40, 40)), BadTile((45, 45)), StopTile((50, 50), event_stoptile_1),
        GoodTile((55, 55)), BadTile((60, 60)), EventTile((65, 65)), BadTile((70, 70)), StopTile((75, 75), event_stoptile_2),
        GoodTile((80, 80)), BadTile((85, 85)), EventTile((90, 90)), BadTile((95, 95)), EventTile((100, 100)),
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
