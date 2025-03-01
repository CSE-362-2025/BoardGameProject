"""
Authors: Bottom Six
Created: 2025/02/18
Last Edited: 2025/02/18
Classes surrounding the in-game events that occur following a landing on a space.
"""
import pygame


class Event:

    def __init__(self, name, description, criteria, result, rarity):
        self.name = name
        self.description = description
        self.criteria = criteria
        self.result = result
        self.rarity = rarity
    
    def meet_criteria(player_stats, criteria):
        return all(player_stats.get(key, 0) >= value for key, value in criteria.items())


class NonDecisionEvent(Event):

    def __init__(self, name, description, criteria, result):
        super().__init__(self, name, description, criteria, result)

    def apply_result(self, player):
        player.update_stats(self.result)


class DecisionEvent(Event):

    def __init__(self, name, description, criteria, result, choices):
        super().__init__(self, name, description, criteria, result)
        
        self.choices = choices

    def apply_result(self, player, choice_idx):
        player.update_stats(self.choices[choice_idx].result)


