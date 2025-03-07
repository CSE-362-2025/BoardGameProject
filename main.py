"""
Author: Bottom Six
Created: 2025/01/24
Last Edited: 2025/02/17
Main function for game: in charge of running the game
"""

import pygame
import sys
import gameManager

#sets what window size is rather than doing something dumb like hardcoding it everywhere (that would be annoying)
windowWidth = 1080 
windowHeight = 720

def main():
    pygame.init()
    display = pygame.time.Clock()
    screen = pygame.display.set_mode((windowWidth, windowHeight), pygame.RESIZABLE)
    manager = gameManager.GameManager(windowWidth, windowHeight)  
    manager.prepGame() #calls the prep game seperately rather than hardcoding all the prep in the main loop where it doesn't belong.

    # Runs the Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False #stops the game
            elif event.type == pygame.MOUSEBUTTONDOWN:
                #Reacts to button clicks
                manager.onClick(screen) 
        manager.run() #Reacts as normal regardless of events
        manager.render(screen) #Draws things
        display.tick(60) #sets the tick and frame rate
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
