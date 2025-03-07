import pygame
from game_manager import GameManager
from board import Board
from player import Player
from ui import UI
from event import Event
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
        events.append(Event(event['name'], event['description'], 
                                    event['choices'], event['rarity'],
                                    event['phase']))

            
    event_stoptile = Event("StopTile 1", "PPT! (+2 Athletic)", [{"text" : "Study (+1 Academic)",
                    "result" : {"bilingual" : 0, 
                                "athletic" : 0, 
                                "academic" : 1, 
                                "military" : 0, 
                                "social" : 0},

                    "criteria" : {"bilingual" : 0, 
                                "athletic" : 0, 
                                "academic" : 0, 
                                "military" : 0, 
                                "social" : 0}
        },

        {"text" : "Go out with friends. (+2 Social -1 Academic)",
                    "result" : {"bilingual" : 0, 
                                "athletic" : 0, 
                                "academic" : 1, 
                                "military" : 0, 
                                "social" : 0},

                    "criteria" : {"bilingual" : 0, 
                                "athletic" : 0, 
                                "academic" : 0, 
                                "military" : 0, 
                                "social" : 0}
        }], None, None)
    

    # Create board with tiles
    tiles = [
        GoodTile(0), BadTile(1), GoodTile(2), BadTile(3), EventTile(4),
        GoodTile(5), BadTile(6), GoodTile(7), BadTile(8), StopTile(9, event_stoptile),
        GoodTile(10), BadTile(11), EventTile(12), BadTile(13), StopTile(14, event_stoptile),
        GoodTile(15), BadTile(16), EventTile(17), BadTile(18), EventTile(19),
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
