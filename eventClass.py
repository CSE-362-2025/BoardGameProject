"""
Authors: Bottom Six
Created: 2025/02/18
Last Edited: 2025/02/18
Classes surrounding the in-game events that occur following a landing on a space.
"""
import pygame


class Events:
    def __init__(self, result):
        match result:
            case 1:
                self.type = "Type1"
            case 2:
                self.type = "Type2"
            case _:
                self.type = "Type3"
        #todo: read info for types from database
        self.query = "What do you do?"
        self.options = [("Option 1", "Outcome 1"), ("Option 2", "Outcome 2")]
        self.result = None

    def click(self, screen):
        b = screen.get_width()/100
        c = screen.get_height()/100
        mouse = pygame.mouse.get_pos()
        i = 0
        a = len(self.options)
        buttonWidth=80/a
        for option in self.options:
            buttonLeft = buttonWidth*i + 10
            if (buttonLeft*b) <= mouse[0] <= ((buttonLeft+(buttonWidth-2))*b) and (72*c) <= mouse[1] <= (88*c):
                self.result = option[1]
                return self.result
            i =+ 1
        return -1

    def drawEvents(self, screen):
        b = screen.get_width()/100
        c = screen.get_height()/100
        pygame.draw.rect(screen, (0, 20, 170), (3*b, 3*c, 94*b, 94*c))
        pygame.draw.rect(screen, (234, 255, 0), (4.5*b, 4.5*c, 91*b, 91*c))
        pygame.draw.rect(screen, (0, 20, 170), (5*b, 5*c, 90*b, 90*c))
        if self.result == None:
            font = pygame.font.Font(size=24)
            text = self.query
            x, y = font.size(text)
            text = font.render(text, True, (255,255,255), None)
            screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))
            i = 0
            a = len(self.options)
            buttonWidth=80/a
            for option in self.options:
                buttonLeft = buttonWidth*i + 10
                buttonCentre = buttonWidth*(i+0.5) + 10
                text = option[0]
                x, y = font.size(text)
                text = font.render(text, True, (0,0,0), None)
                pygame.draw.rect(screen, (255,255,255), (buttonLeft*b, 72*c, (buttonWidth-2)*b, 16*c))
                screen.blit(text, ((buttonCentre)*b-(x/2), 80*c))
                i =+ 1
        else:
            font = pygame.font.Font(size=24)
            text = self.result
            x, y = font.size(text)
            text = font.render(text, True, (255,255,255), None)
            screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))

