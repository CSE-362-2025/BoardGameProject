
import pygame


class Event:

    def __init__(self, name, description, choices, rarity, phase):
        self.name = name
        self.description = description
        self.choices = choices
        self.rarity = rarity
        self.phase = phase
    

    def meet_criteria(self, player_stats):
        return all(player_stats.get(key, 0) >= value for key, value in self.criteria.items())
    
    def get_type(self):
        return self.type

    def apply_result(self, player, choice_idx):
        player.update_stats(self.choices[choice_idx].result)

