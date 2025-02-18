"""
Authors: Bottom Six
Created: 2025/02/14
Last Edited: 2025/02/17
Board Class sets up a list of tiles on a board to help determine tile type the player is on.
"""
import pygame
import playerClass

class Tile:
    def __init__(self, tile_details, tile_num):
        self.type = tile_details[0]
        self.ID = tile_num
        self.x = tile_details[1]
        self.y = tile_details[2]


class Board:
    def __init__(self, tile_list):
        """Initializes a set of tiles of a given type based on the given list"""
        self.Players = []
        self.Players.append(playerClass.Player(0, (255, 255, 0)))
        self.Players.append(playerClass.Player(1, (255, 255, 255)))
        self.currentPlayer = 0
        self.finishedPlayers = []
        self.TileList = []
        tile_num = 0
        for tile in tile_list:
            self.TileList.append(Tile(tile, tile_num))
            tile_num += 1

    def movePlayer(self, dist):
        if len(self.Players) > 0:
            self.Players[self.currentPlayer].pos += dist
            rank = len(self.finishedPlayers)+1
            self.Players.sort(reverse=True, key=lambda p: p.pos)
            for player in self.Players:
                player.rank = rank
                rank += 1
            self.Players.sort(key=lambda p: p.ID)
            if self.Players[self.currentPlayer].pos >= len(self.TileList):
                self.finishedPlayers.append(self.Players.pop(self.currentPlayer))
            if self.currentPlayer >= (len(self.Players)-1):
                self.currentPlayer = 0
            else:
                self.currentPlayer =+ 1
        
    
    def drawBoard(self, surface):
        b = surface.get_width()/100
        c = surface.get_height()/100
        tileSize = [5*b, 5*c]

        for tile in self.TileList:
            match tile.type:
                case "Type1":
                    type = (255, 0, 0)
                case "Type2":
                    type = (0, 98, 255)
                case _:
                    type = (0, 0, 0)
            pygame.draw.rect(surface, type, (tile.x*b, tile.y*c, tileSize[0], tileSize[1]))
            for player in self.Players:
                if tile.ID == player.pos:
                    pygame.draw.rect(surface, player.colour, ((tile.x*b)+(tileSize[0]/4), (tile.y*c)+(tileSize[1]/4), tileSize[0]/2, tileSize[1]/2))
        for player in self.finishedPlayers:
            pygame.draw.rect(surface, player.colour, (90*b, 10*player.rank*c, tileSize[0]/2, tileSize[1]/2))