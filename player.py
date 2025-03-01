"""
Authors: Bottom Six
Created: 2025/02/17
Last Edited: 2025/02/17
Keeps track of player specific stats such as tile and board number
"""
import pygame
import random

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
        self.position += spaces

    def change_stats(self, stats):
        for key in stats:
            self.stats[key] += stats[key]

    def store_event(self, event):
        self.events_played.append(event)

    def get_stats(self):
        return self.stats
    

class ComputerPlayer(Player): 

    def __init__(self, name, stats=None):
        super().__init__(name, stats)

    # Makes a decision based on the event, returns the index of the choice
    def make_decision(self, event):
        return random.randint(0, len(event.choices) - 1)


