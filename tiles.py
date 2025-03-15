class Tile:

    def __init__(self, position, tile_type, screen_position):
        self.position = position
        self.tile_type = tile_type
        self.screen_position = screen_position  

    def get_position(self):
        return self.position
    
    def get_type(self):
        return self.tile_type
        

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
    
    def __init__(self, position, event, paths):
        super().__init__(position, tile_type="StopTile")
        self.event = event
        self.paths = paths


class StartTile(Tile):
    def __init__(self, position):
        super().__init__(position, tile_type="StartTile")
        pass


class EndTile(Tile):
    def __init__(self, position):
        super().__init__(position, tile_type="EndTile")
        pass
