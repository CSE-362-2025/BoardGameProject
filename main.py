"""
Author: Bottom Six
Created: 2025/01/24
Last Edited: 2025/02/17
Main function for game: in charge of running the game
"""

import pygame
import sys
import gameManager

windowWidth = 1080
windowHeight = 720

def main():
    pygame.init()
    display = pygame.time.Clock()
    screen = pygame.display.set_mode((windowWidth, windowHeight))
    manager = gameManager.GameManager(windowWidth, windowHeight)  
    manager.prepGame()

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                manager.onClick(screen)
        manager.run()
        manager.render(screen)
        display.tick(60)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
