"""
Authors: Bottom Six
Created: 2025/02/18
Last Edited: 2025/02/18
Classes surrounding the in-game events that occur following a landing on a space.
"""
import pygame


class Event:

    def __init__(self, name, description, criteria, result):
        self.name = name
        self.description = description
        self.criteria = criteria
        self.result = result
    
    def trigger(player):
        pass


class NonDecisionEvent(Event):

    def __init__(self, name, description, criteria, result):
        super().__init__(name, description, criteria, result)

    def apply_result(player):
        pass


class DecisionEvent(Event):

    def __init__(self, name, description, criteria, result, choices):
        super().__init__(name, description, criteria, result)\
        
        self.choices = choices

    def apply_result(player, choice_idx):
        pass

    def show_choices():
        pass
