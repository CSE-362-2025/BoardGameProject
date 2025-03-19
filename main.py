import pygame
from game_manager import GameManager
from ui import UI


def main():
    # Initialize pygame
    pygame.init()
    
    # Set up display
    pygame.display.set_caption("Board Game")

    # Create UI instance
    ui = UI()

    # Initialize GameManager
    game_manager = GameManager(ui, game_database=None)
    game_manager.start_game()

    ui.game_manager = game_manager

    clock = pygame.time.Clock()
    ui.main_menu()
    ui.update()


    # Main game loop
    running = True
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop when the user closes the window
            elif event.type == pygame.MOUSEBUTTONDOWN:
                ui.handle_click(event.pos)  # Check if dice was clicked

        # Check if the game is over
        if game_manager.is_game_over():
            ui.display_message("Game Over!")  # Display game over message
            pygame.display.update()  # Ensure the last message is displayed
            pygame.time.wait(2000)  # Wait for a couple of seconds before quitting
            running = False

        ui.run()
        # Display the current state
        ui.update()

        # Update the screen (can be flipped to update only parts of the screen)
        pygame.display.flip()  # Update the entire screen
        clock.tick(60)

    pygame.quit()  # Quit the game and close the window


if __name__ == "__main__":
    main()
