"""
Author: Bottom Six
Created: 2025/02/29
Last Edited: 2025/03/18
Tile Class to track the tiles and their information
"""

# Colors for different tile types
TILE_COLORS = {
    "GoodTile": (50, 200, 50),  # Green
    "BadTile": (200, 50, 50),  # Red
    "EventTile": (50, 50, 200),  # Blue
    "StopTile": (200, 200, 50)  # Yellow
}



class Tile:

    def __init__(self, ID, position=(0,0),path = 0, tile_type="None"):
        self.ID = ID #order player travels
        self.position = position #where Tile is
        self.tile_type = tile_type #what Tile is
        self.path = path #which split Tile is on

    def get_position(self):
        return self.position
    
    def get_type(self):
        return self.tile_type
    
    def get_colour(self):
        return TILE_COLORS.get(self.get_type(), (100, 100, 100))  # Default gray if unknown
        

class GoodTile(Tile):

    def __init__(self,ID, position, path=0):
        super().__init__(ID,position, path, tile_type="GoodTile")
        pass


class BadTile(Tile):

    def __init__(self, ID,position, path=0):
        super().__init__(ID,position, path, tile_type="BadTile")
        pass


class EventTile(Tile):

    def __init__(self, ID,position, path=0):
        super().__init__(ID,position, path, tile_type="EventTile")
        pass


class StopTile(Tile):
    
    def __init__(self, ID, position, event, path=0):
        super().__init__(ID, position, path, tile_type="StopTile")
        self.event = event
