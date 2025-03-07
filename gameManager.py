"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Manages the game and tracks when each event should occur
"""
import pygame
import boardClass
import eventClass
import ui
from abc import ABC, abstractmethod
from enum import Enum


class Scene(Enum):
    board = 0
    event = 1
    pause = 2
    title = 3
    mainMenu = 4
    characterMenu = 5
    endScreen = 6


class GameManager:
    def __init__(self, windowWidth, windowHeight):
        self.scene = None
        self.board = None
        self.currentEvents = None
        self.img = None
        self.MainMenu = ui.MainMenu()
        self.pause = ui.PauseMenu()
        self.winW = windowWidth
        self.winH = windowHeight
        self.count = pygame.time.get_ticks()+3000
        self.prep_change = True
    
    def prepGame(self):
        #Set title bar and prep images        
        icon = pygame.image.load("Resources\\RMC-ico.jpg") 
        pygame.display.set_icon(icon)
        pygame.display.set_caption("Scarlets Forever")
        self.img = pygame.transform.scale(pygame.image.load("Resources\\gunsalute-scarlets-mckenzie.jpg"),(self.winW, self.winH))
        self.scene = Scene.title

    def startGame(self):
        #initialize board
        tileList = [("GoodTile", 10, 15), ("BadTile", 20, 15), ("GoodTile", 30, 15), ("EventTile", 40, 15), ("BadTile", 50, 15),  
                    ("GoodTile", 60, 15), ("BadTile", 70, 15), ("BadTile", 80, 15), ("GoodTile", 80, 25), ("EventTile", 80, 35),
                    ("BadTile", 80, 45), ("GoodTile", 80, 55), ("BadTile", 80, 65), ("GoodTile", 80, 75), ("EventTile", 80, 85), 
                    ("BadTile", 70, 85), ("GoodTile", 60, 85), ("BadTile", 50, 85), ("GoodTile", 40, 85), ("EventTile", 30, 85), 
                    ("BadTile", 20, 85), ("GoodTile", 20, 75), ("BadTile", 20, 65), ("GoodTile", 20, 55), ("EventTile", 20, 45),
                    ("BadTile", 20, 35), ("GoodTile", 30, 35), ("BadTile", 40, 35), ("GoodTile", 50, 35), ("EventTile", 60, 35),
                    ("BadTile", 60, 45), ("GoodTile", 60, 55), ("BadTile", 60, 65), ("GoodTile", 50, 65), ("EventTile", 40, 65),
                    ("EndSquare", 40, 55)]
        self.board = boardClass.Board(tileList)

    def run(self):
        """Tracks what happens each round depending on scene"""
        match self.scene:
            case Scene.title:
                if self.count <= pygame.time.get_ticks():
                    self.scene = Scene.mainMenu
                    self.prep_change = False
            case Scene.board:
                if self.prep_change:
                    if self.count <= pygame.time.get_ticks():
                        self.scene = Scene.event
                        self.prep_change = False
                elif self.board.gameOver():
                    self.scene = Scene.endScreen
            case Scene.event:
                if self.prep_change:
                    if self.count <= pygame.time.get_ticks():
                        self.scene = Scene.board
                        self.prep_change = False
                        self.currentEvents = None
                        self.board.nextPlayer()
                else:
                    results = self.currentEvents.run()
                    if results != -1:
                        self.count = pygame.time.get_ticks()+3000
                        self.prep_change = True
            case _:
                pass


    def onClick(self, screen):
        """Tracks what happens depending on scene when a click occurs"""
        match self.scene:
            case Scene.title:
                self.scene = Scene.mainMenu
                self.prep_change = False
            case Scene.mainMenu:
                result = self.MainMenu.mainmenuClick(screen)
                if result != -1:
                    match result:
                        case 0:
                            self.startGame()
                            self.scene = Scene.board
                        case 1:
                            self.scene = Scene.pause
                        case 2:
                            self.startGame()
                            self.scene = Scene.board
                        case 3:
                            self.scene = Scene.characterMenu
            
            case Scene.pause:
                result = self.pause.menuClick(screen)
                if result != -1:
                    match result:
                        case 0:
                            self.scene = Scene.board
                        case 1:
                            self.scene = Scene.characterMenu
                        case 2:
                            pygame.event.post(pygame.event.Event(pygame.QUIT))
                        case 3:
                            self.scene = Scene.characterMenu

            case Scene.board:
                if not self.prep_change:
                    result = ui.diceClick(screen, self.board)
                    if result != -1:
                        self.currentEvents = eventClass.Events(result)
                        self.count = pygame.time.get_ticks()+1000
                        self.prep_change = True
                    result = ui.menuClick(screen)
                    if result == 1:
                        self.scene = Scene.pause
                else:
                    self.scene = Scene.event
                    self.prep_change = False

            case Scene.event:
                if not self.prep_change:
                    result = self.currentEvents.click(screen)
                    if result != -1:
                        self.count = pygame.time.get_ticks()+3000
                        self.prep_change = True
                else:
                    self.scene = Scene.board
                    self.prep_change = False
                    self.currentEvents = None
                    self.board.nextPlayer()
            case _:
                pass


    def render(self, screen):
        """Manages rendering of the game depending on scene"""
        if ((self.img.get_width() != screen.get_width()) or (self.img.get_height() != screen.get_height())):
            self.img = pygame.transform.scale(pygame.image.load("Resources\\gunsalute-scarlets-mckenzie.jpg"),(screen.get_width(), screen.get_height()))
        screen.blit(self.img, (0,0)) 
        match self.scene:
            case Scene.title:
                font = pygame.font.Font(size=30)
                text = 'Bottom Six Presents: [Insert Name Here]'
                x, y = font.size(text)
                text = font.render(text, True, (0,0,0), None)
                screen.blit(text, (screen.get_width()/2-x/2, y/2))
            case Scene.mainMenu:
                self.MainMenu.mainmenuDraw(screen)
            case Scene.board:
                self.board.drawBoard(screen)
                if not self.prep_change:
                    ui.diceButton(screen)
                    ui.menuButton(screen)
            case Scene.pause:
                self.pause.menuDraw(screen)
            case Scene.event:
                self.board.drawBoard(screen)
                self.currentEvents.drawEvents(screen)
            case Scene.endScreen:
                self.board.drawBoard(screen)
                font = pygame.font.Font(size=64)
                text = 'Game Over'
                x, y = font.size(text)
                text = font.render(text, True, (0,0,0), None)
                screen.blit(text, (screen.get_width()/2-x/2, screen.get_height()/2-y/2))
            case _:
                pass
        pygame.display.flip()

class Scenes(ABC):
    pass