class Tile:

    def __init__(self, position, tile_type):
        self.position = position
        self.tile_type = tile_type

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
    
    def __init__(self, position, event):
        super().__init__(position, tile_type="StopTile")
        self.event = event
