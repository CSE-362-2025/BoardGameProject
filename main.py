import pygame
import sys
import boardClass
import playerClass
import ui

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    #Set title bar and prep images
    pygame.display.set_caption("Scarlets Forever")
    icon = pygame.image.load("Resources\\RMC-ico.jpg") 
    pygame.display.set_icon(icon)
    img = pygame.transform.scale(pygame.image.load("Resources\\gunsalute-scarlets-mckenzie.jpg"),(640,480))
    
    #initialize board
    tileList = [("Type1", 5, 15), ("Type2", 15, 15), ("Type1", 25, 15), ("Type2", 35, 15), ("Type3", 45, 15),
                ("Type1", 5, 25), ("Type2", 15, 25), ("Type1", 25, 25), ("Type2", 35, 25), ("Type3", 45, 25)]
    board = boardClass.Board(tileList)


    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                ui.diceClick(screen, board)

        screen.blit(img, (0,0))  # Fill screen with image
        board.drawBoard(screen)
        ui.diceButton(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
