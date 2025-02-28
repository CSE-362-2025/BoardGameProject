"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Keeps track of player specific stats such as tile and board number
"""
import pygame

class Player:
    def __init__(self, name, stats=None):

        self.name = name
        self.position = 0

        # can pass in stats to set them, otherwise default to 0 for now
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

    def hop(self):
        pass

    def change_stats(self, stats):
        pass

    def apply_event(self, event):
        pass

    def choose_option(self, event, choice_idx):
        pass

    def get_stats(self):
        
        return self.stats
    


