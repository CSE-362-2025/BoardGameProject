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
        self.events_played = []

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

    def move(self, spaces):
        pass

    def change_stats(self, stats):
        pass

    def store_event(self, event):
        pass

    def get_stats(self):
        return self.stats
    

class ComputerPlayer(Player): 

    def __init__(self, name, stats=None):
        super().__init__(name, stats)
        pass

    # Makes a decision based on the event, returns the index of the choice
    def make_decision(self, event):
        pass


