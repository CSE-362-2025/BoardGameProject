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

    def __init__(self, position, screen_position, tile_type):
        self.position = position
        self.tile_type = tile_type
        self.screen_position = screen_position  

    def get_position(self):
        return self.position
    
    def get_type(self):
        return self.tile_type
    
    def get_screen_pos(self):
        return self.screen_position
        
    def get_colour(self):
        return TILE_COLORS.get(self.get_type(), (100, 100, 100))  # Default gray if unknown

class GoodTile(Tile):

    def __init__(self, position):
        super().__init__(position, tile_type="GoodTile")
        pass


class BadTile(Tile):

    def __init__(self, position):
        super().__init__(position, tile_type="BadTile")
        pass


class EventTile(Tile):

    def __init__(self, position):
        super().__init__(position, tile_type="EventTile")
        pass


class StopTile(Tile):
    
    def __init__(self, position, screen_position, event, paths=None):
        super().__init__(position, screen_position, tile_type="StopTile")
        self.event = event
        self.paths = paths


class StartTile(Tile):
    def __init__(self, position, screen_position):
        super().__init__(position, screen_position, tile_type="StartTile")
        pass


class EndTile(Tile):
    def __init__(self, position, screen_position):
        super().__init__(position, screen_position, tile_type="EndTile")
        pass
