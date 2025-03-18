
import pygame
import random

PLAYER_RADIUS = 25
FONT_COLOR = (255, 255, 255)  # White text

class Player:

    def __init__(self, name, color, stats=None, image=None):

        self.name = name
        self.color = color
        self.position = 0
        self.events_played = []
        self.has_moved = True
        self.image=image
        self.path = 0

        # can pass in stats to set them, otherwise default to 0 for now
        if stats is not None:
            self.stats = stats

        else:
            self.stats = {
                "bilingual": 5,
                "athletic": 5,
                "military": 5,
                "academic": 5,
                "social": 5,
            }

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
    
    def draw(self, screen, position):   
        screen_width = screen.get_width()/100
        screen_height = screen.get_height()/100
        font = pygame.font.Font(None, 16)
        mid = position[2]
        if self.image:
            playerimg = pygame.transform.scale(pygame.image.load(self.image),(PLAYER_RADIUS,PLAYER_RADIUS))
            screen.blit(playerimg,((position[0])*screen_width-PLAYER_RADIUS/2, (position[1])*screen_height-PLAYER_RADIUS/2))
        else:
            pygame.draw.circle(screen, self.color, ((position[0])*screen_width, (position[1])*screen_height), PLAYER_RADIUS)

        # Draw player name or symbol above the circle
        player_text = font.render(self.name[-1], True, FONT_COLOR)
        player_text_rect = player_text.get_rect(center=((position[0]-mid)*screen_width, (position[1] - mid)*screen_height))
        screen.blit(player_text, player_text_rect)

    

class ComputerPlayer(Player): 

    def __init__(self, name, stats=None):
        super().__init__(name, stats)

    # Makes a decision based on the event, returns the index of the choice
    def make_decision(self, event):
        return random.randint(0, len(event.choices) - 1)
