"""
Authors: Bottom Six
Last Edit: 2025/02/17
Keeps track of the user interfact and runs event dependant on the results
"""
import pygame 
import random


def diceClick(screen, board):
    dicePos = [90, 90, 100, 100]
    diceLeft, diceTop, diceRight, diceBottom = dicePos
    b = screen.get_width()/100
    c = screen.get_height()/100
    mouse = pygame.mouse.get_pos()
    if (diceLeft*b) <= mouse[0] <= (diceRight*b) and (diceTop*c) <= mouse[1] <= (diceBottom*c):
        board.movePlayer(random.randint(1,6))


def diceButton(screen):
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