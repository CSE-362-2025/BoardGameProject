"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Manages the game and tracks when each event should occur
"""
import pygame
import boardClass
import ui
from abc import ABC, abstractmethod
from enum import Enum


class Scene(Enum):
    board = 0
    event = 1
    title = 3
    mainMenu = 4
    characterMenu = 5
    endSceen = 6


class GameManager:
    def __init__(self, windowWidth, windowHeight):
        self.scene = None
        self.board = None
        self.img = None
        self.winW = windowWidth
        self.winH = windowHeight
    
    def prepGame(self):
        #Set title bar and prep images        
        icon = pygame.image.load("Resources\\RMC-ico.jpg") 
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Scarlets Forever")
        self.img = pygame.transform.scale(pygame.image.load("Resources\\gunsalute-scarlets-mckenzie.jpg"),(self.winW, self.winH))
        self.scene = Scene.title

    def startGame(self):
        #initialize board
        tileList = [("Type1", 5, 15), ("Type2", 15, 15), ("Type1", 25, 15), ("Type2", 35, 15), ("Type3", 45, 15),
                ("Type1", 5, 25), ("Type2", 15, 25), ("Type1", 25, 25), ("Type2", 35, 25), ("Type3", 45, 25),
                ("Type1", 5, 35), ("Type2", 15, 35), ("Type1", 25, 35), ("Type2", 35, 35), ("Type3", 45, 35), 
                ("Type1", 5, 45), ("Type2", 15, 45), ("Type1", 25, 45), ("Type2", 35, 45), ("Type3", 45, 45), 
                ("Type1", 5, 55), ("Type2", 15, 55), ("Type1", 25, 55), ("Type2", 35, 55), ("Type3", 45, 55)]
        self.board = boardClass.Board(tileList)


    def onClick(self, screen):
        ui.diceClick(screen, self.board)


    def render(self, screen):
        screen.blit(self.img, (0,0))  # Fill screen with image
        self.board.drawBoard(screen)
        ui.diceButton(screen)
        pygame.display.flip()

class Scenes(ABC):
    pass