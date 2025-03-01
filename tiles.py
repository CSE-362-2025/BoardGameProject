class Tile:

    def __init__(self, position, tile_type):
        self.position = position
        self.tile_type = tile_type

    def get_position(self):
        return self.position
    
    def get_tile_type(self):
        return self.tile_type
        

class GoodTile(Tile):

    def __init__(self, position, tile_type):
        super().__init__(position, tile_type)
        pass


class BadTile(Tile):

    def __init__(self, position, tile_type):
        super().__init__(position, tile_type)
        pass


class EventTile(Tile):

    def __init__(self, position, tile_type):
        super().__init__(position, tile_type)
        pass


class StopTile(Tile):
    
    def __init__(self, position, tile_type, event):
        super().__init__(position, tile_type)
        self.event = event
