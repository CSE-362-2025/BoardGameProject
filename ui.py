"""
Authors: Bottom Six
Last Edit: 2025/02/17
Keeps track of the user interfact and runs event dependant on the results
A variety of buttons and other useful helper codes - could be refactored to improve readability
"""
import pygame 
import random


def diceClick(screen, board):
    """Tracks what happens if dice is clicked"""
    dicePos = [90, 90, 100, 100]
    diceLeft, diceTop, diceRight, diceBottom = dicePos
    b = screen.get_width()/100
    c = screen.get_height()/100
    mouse = pygame.mouse.get_pos()
    if (diceLeft*b) <= mouse[0] <= (diceRight*b) and (diceTop*c) <= mouse[1] <= (diceBottom*c):
        return board.movePlayer(random.randint(1,6))
    return -1


def diceButton(screen):
    """Tracks what dice botton looks like (mouseover and not mouseover)"""
    dicePos = [90, 90, 100, 100]
    diceLeft, diceTop, diceRight, diceBottom = dicePos
    b = screen.get_width()/100
    c = screen.get_height()/100
    width = diceRight-diceLeft
    height = diceBottom-diceTop
    mouse = pygame.mouse.get_pos()
    if (diceLeft*b) <= mouse[0] <= (diceRight*b) and (diceTop*c) <= mouse[1] <= (diceBottom*c):
        pygame.draw.rect(screen, (255,255,0), (diceLeft*b, diceTop*c, width*b, height*c))
    else:
        pygame.draw.rect(screen, (255,255,255), (diceLeft*b, diceTop*c, width*b, height*c))


def menuClick(screen): 
    """Tracks if pause menu button is clicked"""
    buttonPos = [90, 0, 100, 10]
    buttonLeft, buttonTop, buttonRight, buttonBottom = buttonPos
    b = screen.get_width()/100
    c = screen.get_height()/100
    mouse = pygame.mouse.get_pos()
    if (buttonLeft*b) <= mouse[0] <= (buttonRight*b) and (buttonTop*c) <= mouse[1] <= (buttonBottom*c):
        return 1
    return -1


def menuButton(screen):
    """Tracks what pause menu button looks like"""
    buttonPos = [90, 0, 100, 10]
    buttonLeft, buttonTop, buttonRight, buttonBottom = buttonPos
    b = screen.get_width()/100
    c = screen.get_height()/100
    width = buttonRight-buttonLeft
    height = buttonBottom-buttonTop
    mouse = pygame.mouse.get_pos()
    if (buttonLeft*b) <= mouse[0] <= (buttonRight*b) and (buttonTop*c) <= mouse[1] <= (buttonBottom*c):
        pygame.draw.rect(screen, (255,255,0), (buttonLeft*b, buttonTop*c, width*b, height*c))
    else:
        pygame.draw.rect(screen, (255,255,255), (buttonLeft*b, buttonTop*c, width*b, height*c))

class PauseMenu():
    """The Pause Menu. Currently has minimal options as a. DB was not yet done and b. higher priority items"""
    def __init__(self):
        self.options = [("Resume", 0), ("Settings", 1), ("Save & Quit", 2), ("Characters", 3)]

    def menuDraw(self, screen):
        """Tracks what the menu looks like"""
        b = screen.get_width()/100
        c = screen.get_height()/100
        pygame.draw.rect(screen, (0, 20, 170), (3*b, 3*c, 94*b, 94*c))
        pygame.draw.rect(screen, (234, 255, 0), (4.5*b, 4.5*c, 91*b, 91*c))
        pygame.draw.rect(screen, (0, 20, 170), (5*b, 5*c, 90*b, 90*c))
        font = pygame.font.Font(size=36)
        text = "PAUSE"
        x, y = font.size(text)
        text = font.render(text, True, (255,255,255), None)
        screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))
        i = 0
        j = 0
        a = len(self.options)
        buttonWidth=20
        for option in self.options:
            buttonLeft = buttonWidth*2*i + 20
            buttonTop = buttonWidth*2*j + 20
            text = option[0]
            x, y = font.size(text)
            text = font.render(text, True, (0,0,0), None)
            pygame.draw.rect(screen, (255,255,255), (buttonLeft*b, buttonTop*c, (buttonWidth)*b, buttonWidth*c))
            screen.blit(text, ((buttonLeft+10)*b-(x/2), (buttonTop+10)*c))
            if i == 1:
                i = 0
                j =+ 1
            else:
                i =+ 1


    def menuClick(self, screen):
        """Tracks what menu button is clicked (if any)"""
        b = screen.get_width()/100
        c = screen.get_height()/100
        mouse = pygame.mouse.get_pos()
        i = 0
        j = 0
        a = len(self.options)
        buttonWidth=20
        for option in self.options:
            buttonLeft = buttonWidth*2*i + 20
            buttonTop = buttonWidth*2*j + 20
            if (buttonLeft*b) <= mouse[0] <= ((buttonLeft+(buttonWidth))*b) and (buttonTop*c) <= mouse[1] <= ((buttonTop+buttonWidth)*c):
                result = option[1]
                return result
            if i == 1:
                i = 0
                j =+ 1
            else:
                i =+ 1
        return -1
    




def mainmenuClick(screen): 
    """Tracks if main menu button is clicked"""
    buttonPos = [90, 0, 100, 10]
    buttonLeft, buttonTop, buttonRight, buttonBottom = buttonPos
    b = screen.get_width()/100
    c = screen.get_height()/100
    mouse = pygame.mouse.get_pos()
    if (buttonLeft*b) <= mouse[0] <= (buttonRight*b) and (buttonTop*c) <= mouse[1] <= (buttonBottom*c):
        return 1
    return -1


def mainmenuButton(screen):
    """Tracks what main menu button looks like"""
    buttonPos = [90, 0, 100, 10]
    buttonLeft, buttonTop, buttonRight, buttonBottom = buttonPos
    b = screen.get_width()/100
    c = screen.get_height()/100
    width = buttonRight-buttonLeft
    height = buttonBottom-buttonTop
    mouse = pygame.mouse.get_pos()
    if (buttonLeft*b) <= mouse[0] <= (buttonRight*b) and (buttonTop*c) <= mouse[1] <= (buttonBottom*c):
        pygame.draw.rect(screen, (255,255,0), (buttonLeft*b, buttonTop*c, width*b, height*c))
    else:
        pygame.draw.rect(screen, (255,255,255), (buttonLeft*b, buttonTop*c, width*b, height*c))


class MainMenu():
    """The Main Menu - Same as with pause menu, was waiting on DB and high priority features"""
    def __init__(self):
        self.options = [("New Game", 0), ("Settings", 1), ("Load Game", 2), ("Characters", 3)]

    def mainmenuDraw(self, screen):
        """Tracks what menu looks like"""
        b = screen.get_width()/100
        c = screen.get_height()/100
        pygame.draw.rect(screen, (0, 20, 170), (3*b, 3*c, 94*b, 94*c))
        pygame.draw.rect(screen, (234, 255, 0), (4.5*b, 4.5*c, 91*b, 91*c))
        pygame.draw.rect(screen, (0, 20, 170), (5*b, 5*c, 90*b, 90*c))
        font = pygame.font.Font(size=36)
        text = "Main Menu"
        x, y = font.size(text)            
        text = font.render(text, True, (255,255,255), None)
        screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))
        i = 0
        j = 0
        a = len(self.options)
        buttonWidth=20
        for option in self.options:
            buttonLeft = buttonWidth*2*i + 20
            buttonTop = buttonWidth*2*j + 20
            text = option[0]
            x, y = font.size(text)
            text = font.render(text, True, (0,0,0), None)
            pygame.draw.rect(screen, (255,255,255), (buttonLeft*b, buttonTop*c, (buttonWidth)*b, buttonWidth*c))
            screen.blit(text, ((buttonLeft+10)*b-(x/2), (buttonTop+10)*c))
            if i == 1:
                i = 0
                j =+ 1
            else:
                i =+ 1


    def mainmenuClick(self, screen):
        """Tracks which button is pressed (if any)"""
        b = screen.get_width()/100
        c = screen.get_height()/100
        mouse = pygame.mouse.get_pos()
        i = 0
        j = 0
        a = len(self.options)
        buttonWidth=20
        for option in self.options:
            buttonLeft = buttonWidth*2*i + 20
            buttonTop = buttonWidth*2*j + 20
            if (buttonLeft*b) <= mouse[0] <= ((buttonLeft+(buttonWidth))*b) and (buttonTop*c) <= mouse[1] <= ((buttonTop+buttonWidth)*c):
                result = option[1]
                return result
            if i == 1:
                i = 0
                j =+ 1
            else:
                i =+ 1
        return -1