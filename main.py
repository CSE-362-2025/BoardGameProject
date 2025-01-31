import pygame
import sys
# Raymond was here :D!!

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Scarlets Forever")
    img = pygame.transform.scale(pygame.image.load('Resources\gunsalute-scarlets-mckenzie.jpg'),(0,0))

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(img, (0,0))  # Fill screen with white
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
