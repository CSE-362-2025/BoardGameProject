class Tile:

    def __init__(self, position, tile_type):
        self.position = position
        self.tile_type = tile_type

    def get_position(self):
        return self.position
    
    def get_tile_type(self):
        return self.tile_type
        

class GoodTile(Tile):

    def __init__(self, position, tile_type, message, effect):
        super().__init__(position, tile_type)
        self.message = message
        self.effect = effect

    def apply_effect(player):
        pass


class BadTile(Tile):

    def __init__(self, position, tile_type, message, effect):
        super().__init__(position, tile_type)
        self.message = message
        self.effect = effect

    def apply_effect(player):
        pass

class EventTile(Tile):

    def __init__(self, position, tile_type, event):
        super().__init__(position, tile_type)
        self.event = event

    def trigger_event(player):
        pass


class StopTile(Tile):
    
    def __init__(self, position, tile_type, event):
        super().__init__(position, tile_type)
        self.event = event

    def trigger_event(player):
        pass