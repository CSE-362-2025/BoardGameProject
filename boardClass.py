"""
Authors: Bottom Six
Last Edit: 2025/02/14
Board Class sets up a list of tiles on a board to help determine tile type the player is on.
"""
import pygame
import math

class Tile:
    def __init__(self, type, tile_num):
        self.type = type
        self.ID = tile_num


class Board:
    def __init__(self, tile_list):
        """Initializes a set of tiles of a given type based on the given list"""
        self.TileList = []
        tile_num = 0
        for tile in tile_list:
            self.TileList.append(Tile(tile, tile_num))
            tile_num += 1

    def playerTile(self, position):
        currentTile = self.TileList[position]
        return(currentTile.type, currentTile.ID)
    
    def drawBoard(self, surface):
        a = len(self.TileList)
        b = surface.get_width()/(a/2)
        c = surface.get_height()/(a+1)
        tilePlace = [-b, surface.get_height()/(2*a), surface.get_width()/(2*a), surface.get_height()/(2*a)]
        for tile in self.TileList:
        
            match tile.type:
                case "Type1":
                    type = (255, 0, 0)
                case "Type2":
                    type = (0, 98, 255)
                case _:
                    type = (0, 0, 0)   
            if (tile.ID < a/2): 
                    tilePlace[0] += b
            else:
                    tilePlace[1] += c
            pygame.draw.rect(surface, type, (tilePlace[0], tilePlace[1], tilePlace[2], tilePlace[3]))


    """

        for tile in self.TileList:
            match tile.type:
                case "Type1":
                    type = (255, 0, 0)
                case "Type2":
                    type = (0, 98, 255)
                case _:
                    type = (0, 0, 0)    
            pygame.draw.rect(surface, type, (tilePlace[0], tilePlace[1], tilePlace[2], tilePlace[3]))
            if (tile.ID % 5) == 0:
                tilePlace[0] += -(4*b)
                tilePlace[1] += c
            else:
                tilePlace[0] += b
            """


if __name__ == '__main__':
    tileList = ["Type1", "Type2", "Type1", "Type2", "Type3","Type1", "Type2", "Type1", "Type2", "Type3"]
    board = Board(tileList)
    print(board.playerTile(4))

