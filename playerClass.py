"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Keeps track of player specific stats such as tile and board number
"""
import pygame

class Player:
    def __init__(self, ID, colour, name="Player", stats=None):
        self.name = name
        self.ID = ID
        self.colour = colour
        self.pos = 0
        self.rank = 0

        # can pass in stats to set them, otherwise default to 0
        if stats is not None:
            self.stats = stats

        else:
            self.stats = {
                "bilingual": 0,
                "athletic": 0,
                "military": 0,
                "academic": 0,
                "social": 0,
            }
    
    def __lt__(self, other):
        return self.pos < other.pos
    
    def render(self, screen, position, tile):
        b = screen.get_width()/100
        c = screen.get_height()/100
        if tile == False:
            pygame.draw.rect(screen, self.colour, ((position[0]*b)+(5/4*b), (position[1]*c)+(5/4*c), 2.5*b, 2.5*c))
        else:
            pygame.draw.rect(screen, self.colour, ((position.x*b)+(5/4*b), (position.y*c)+(5/4*c), 2.5*b, 2.5*c))

