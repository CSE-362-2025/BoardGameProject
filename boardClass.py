"""
Authors: Bottom Six
Created: 2025/02/14
Last Edited: 2025/02/17
Board Class sets up the board and helps determine the tile type the player is on.
"""
import pygame
import playerClass

class Tile:
    #The Tile object tracks its position to render itself and track where player should render
    def __init__(self, tile_details, tile_num):
        self.type = tile_details[0]
        self.ID = tile_num
        self.x = tile_details[1]
        self.y = tile_details[2]
        #self.colour used for rendering, could use enum but being deleted anyways cause modular objects are bad according to new overlords
        match self.type:
            case "BadTile":
                self.colour = (255, 0, 0)
            case "GoodTile":
                self.colour = (0, 255, 0)
            case "EventTile":
                self.colour = (0, 98, 255)
            case _:
                self.colour = (0,0,0)

    def draw(self, screen):
        #draws the tile as will be determined by design team
        b = screen.get_width()/100
        c = screen.get_height()/100
        pygame.draw.rect(screen, self.colour, (self.x*b, self.y*c, 5*b, 5*c))


#added despite only functionality being colour or smthing - they do nothing anyways
class GoodTile(Tile):
    pass

class BadTile(Tile):
    pass

class EventTile(Tile):
    pass

class StopTile(Tile):
    pass


class Board:
    def __init__(self, tile_list):
        """
        Initializes a set of tiles of a given type based on the given list
        Adds players as per database and player add functions, not yet added here or in overlord's code because... 
        well
        overlord wanted to redo the stuff that was made and delete any sort of customizability. So temp player adding will continue ig
        """
        self.Players = []
        self.Players.append(playerClass.Player(0, (255, 255, 0), "John"))
        self.Players.append(playerClass.Player(1, (255, 255, 255)))
        self.currentPlayer = 0
        self.finishedPlayers = []
        self.TileList = []
        tile_num = 0
        for tile in tile_list:
            self.TileList.append(Tile(tile, tile_num))
            tile_num += 1

    def movePlayer(self, dist):
        """Moves the player position on the board - rolls dice and stuff ig"""
        if len(self.Players) > 0:
            self.Players[self.currentPlayer].pos += dist
            rank = len(self.finishedPlayers)+1
            self.Players.sort(reverse=True, key=lambda p: p.pos)
            for player in self.Players:
                player.rank = rank
                rank += 1
            self.Players.sort(key=lambda p: p.ID)
            return self.TileList[self.Players[self.currentPlayer].pos].type
            

    def nextPlayer(self):
        """Changes Player to next one in turn order"""
        if self.Players[self.currentPlayer].pos >= len(self.TileList):
            self.finishedPlayers.append(self.Players.pop(self.currentPlayer))
        if self.currentPlayer >= (len(self.Players)-1):
            self.currentPlayer = 0
        else:
            self.currentPlayer =+ 1
        
    def gameOver(self):
        """Temp function to know when game is over"""
        if self.Players == []:
            return True
        return False
    
    def drawBoard(self, surface):
        """Draws board and tells tiles and players to render themselves."""
        b = surface.get_width()/100
        c = surface.get_height()/100
        tileSize = [5*b, 5*c]
        if len(self.Players) != 0:
            for tile in self.TileList:
                tile.draw(surface)
                for player in self.Players:
                    if tile.ID == player.pos:
                        player.render(surface, tile, True)
        for player in self.finishedPlayers:
            player.render(surface, (90, 10*player.rank), False)