
import pygame


class Event:

    def __init__(self, name, description, criteria, result, rarity, type):
        self.name = name
        self.description = description
        self.criteria = criteria
        self.result = result
        self.rarity = rarity
        self.type = type  # "Decision" or "Static"
    

    def meet_criteria(self, player_stats):
        return all(player_stats.get(key, 0) >= value for key, value in self.criteria.items())
    
    def get_type(self):
        return self.type


class StaticEvent(Event):

    def __init__(self, name, description, criteria, result, rarity):
        super().__init__(name, description, criteria, result, rarity, type="Static")

    def apply_result(self, player):
        player.change_stats(self.result)

class DecisionEvent(Event):

    def __init__(self, name, description, criteria, choices, rarity):
        super().__init__(name, description, criteria, None, rarity, type="Decision")
        
        self.choices = choices

    def apply_result(self, player, choice_idx):
        player.update_stats(self.choices[choice_idx].result)


