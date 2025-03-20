
import pygame
import random

class Player:

    def __init__(self, name, color, stats=None):

        self.name = name
        self.color = color
        self.position = 0
        self.events_played = []
        self.has_moved = True

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

        # add attributes to match latest class diagram
        self.next_pos: int = 0
        self.on_alt_path: bool = False
        self.branch: bool = False

    def move(self, spaces):
        self.position += spaces

    def change_stats(self, stats):
        for key in stats:
            self.stats[key] += stats[key]

    def store_event(self, event, choice_idx=None):
        if choice_idx is not None:
            self.events_played.append((event, choice_idx))
        else:
            self.events_played.append((event, None))

    def get_stats(self):
        return self.stats


class ComputerPlayer(Player):

    def __init__(self, name, stats=None):
        super().__init__(name, stats)

    # Makes a decision based on the event, returns the index of the choice
    def make_decision(self, event):
        return random.randint(0, len(event.choices) - 1)


