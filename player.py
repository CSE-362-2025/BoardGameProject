
import pygame
import random

class Player:

    def __init__(self, name, color, stats=None):

        self.name = name
        self.color = color
        self.position = 0
        self.events_played = []
        self.has_moved = True

        # For branching
        self.branch = False
        self.next_pos = None
        self.on_alt_path = False

        # can pass in stats to set them, otherwise default to 0 for now
        if stats is not None:
            self.stats = stats

        else:
            self.stats = {  # Caps at 10 and can't go below 0
                "bilingual": 5,
                "athletic": 5,
                "military": 5,
                "academic": 5,
                "social": 5,
            }

    def move(self, spaces):
        self.position += spaces

    def change_stats(self, stats):

        # keeps it above 0 and below 10
        for key in stats:
            if self.stats[key] + stats[key] > 10:
                self.stats[key] = 10
                continue

            elif self.stats[key] + stats[key] < 0:
                self.stats[key] = 0
                continue
    
            self.stats[key] += stats[key]

    def store_event(self, event, choice_idx=None):
        if choice_idx is not None:
            self.events_played.append((event.id, choice_idx))
        else:
            self.events_played.append((event.id, None))

    def get_stats(self):
        return self.stats
    

class ComputerPlayer(Player): 

    def __init__(self, name, stats=None):
        super().__init__(name, stats)

    # Makes a decision based on the event, returns the index of the choice
    def make_decision(self, event):
        return random.randint(0, len(event.choices) - 1)


