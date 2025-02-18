"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Keeps track of player specific stats such as tile and board number
"""

class Player:
    def __init__(self, ID, colour):
        self.ID = ID
        self.pos = 0
        self.colour = colour
        self.rank = 0
    
    def __lt__(self, other):
        return self.pos < other.pos