"""
Authors: Bottom Six
Created: 2025/02/14
Last Edited: 2025/03/18
The player class tracks the player information, and has some functions to help manipulate and render the player
"""
import pygame
import random

FONT_COLOR = (255, 255, 255)  # White text

class Player:

    def __init__(self, name, color, stats=None, image=None):

        self.name = name
        self.color = color
        self.position = 0
        self.curr_pos_draw = [0,0]
        self.next_pos_draw = [0,0]
        self.events_played = []
        self.has_moved = True
        self.image=image

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

    def draw(self, screen, position):   
        screen_width = screen.get_width()/100
        screen_height = screen.get_height()/100
        PLAYER_RADIUS = position[2][1]
        font = pygame.font.Font(None, 16)
        self.next_pos_draw = [(position[0])*screen_width,(position[1])*screen_height]
        if self.next_pos_draw[0]-3.1 < self.curr_pos_draw[0] <self.next_pos_draw[0]+3.1:
            self.curr_pos_draw[0] = self.next_pos_draw[0]       
        else:
            if self.next_pos_draw[0] < self.curr_pos_draw[0]:
                self.curr_pos_draw[0] = self.curr_pos_draw[0]-3
            else:
                self.curr_pos_draw[0] = self.curr_pos_draw[0]+3
        if self.next_pos_draw[1]-3.1 < self.curr_pos_draw[1] <self.next_pos_draw[1]+3.1:
            self.curr_pos_draw[1] = self.next_pos_draw[1]
        else:
            if self.next_pos_draw[1] < self.curr_pos_draw[1]:
                self.curr_pos_draw[1] = self.curr_pos_draw[1]-3
            else:
                self.curr_pos_draw[1] = self.curr_pos_draw[1]+3
        if self.image:
            playerimg = pygame.transform.scale(pygame.image.load(self.image),(PLAYER_RADIUS,PLAYER_RADIUS*2))
            screen.blit(playerimg,(self.curr_pos_draw[0]-PLAYER_RADIUS/2, self.curr_pos_draw[1]-PLAYER_RADIUS*1.5))
        else:
            pygame.draw.circle(screen, self.color, (self.curr_pos_draw[0], self.curr_pos_draw[1]), PLAYER_RADIUS)

    

class ComputerPlayer(Player): 

    def __init__(self, name, stats=None):
        super().__init__(name, stats)

    # Makes a decision based on the event, returns the index of the choice
    def make_decision(self, event):
        return random.randint(0, len(event.choices) - 1)


