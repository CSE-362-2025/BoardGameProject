"""
Authors: Bottom Six
Last Edit: 2025/02/17
Keeps track of player specific stats such as tile and board number
"""

class Player:
    def __init__(self, ID, colour):
        self.ID = ID
        self.pos = 0
        self.colour = colour