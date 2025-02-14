"""
Authors: Bottom Six
Last Edit: 2025/02/14
Board Class sets up a list of tiles on a board to help determine tile type the player is on.
"""


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


if __name__ == '__main__':
    tileList = ["Type1", "Type2", "Type1", "Type2", "Type3"]
    board = Board(tileList)
    print(board.playerTile(4))

