"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Keeps track of player specific stats such as tile and board number
"""

class Player:
    def __init__(self, ID, colour, name="Player"):
        self.name = name
        self.ID = ID
        self.colour = colour
        self.pos = 0
        self.rank = 0
    
    def __lt__(self, other):
        return self.pos < other.pos