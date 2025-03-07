"""
Authors: Bottom Six
Created: 2025/02/18
Last Edited: 2025/02/18
Classes surrounding the in-game events that occur following a landing on a space.
"""
import pygame


class Events:
    """Tracks events - Need to grab code from Gallant who decided to redo everything else instead of the bit they monopolized the first meeting talking about"""
    def __init__(self, result):
        """Preps the event"""
        self.type = result
        #todo: read info for types from database - will be read from database, no reaction even - just remove outcomes
        self.result = None
        self.options = []
        if self.type == "EventTile":
            self.query = "What do you do? - To be grabbed from database"
            self.options = [("This is option 1", "This is what happens if you choose option 1"),("This is option 2", "This is what happens if you choose option 2")]
        else: 
            self.query = "An event occurs! "+self.type

    def click(self, screen):
        """Reacts on a click"""
        if len(self.options)>0:
            b = screen.get_width()/100
            c = screen.get_height()/100
            mouse = pygame.mouse.get_pos()
            i = 0
            a = len(self.options)
            buttonWidth=80/a
            for option in self.options:
                buttonLeft = buttonWidth*i + 10
                if (buttonLeft*b) <= mouse[0] <= ((buttonLeft+(buttonWidth-2))*b) and (72*c) <= mouse[1] <= (88*c):
                    #todo: insert event logic because someone decided only to do work the weekend before sdd was due
                    self.result = option[1]
                    #call changes to player stats
                    return self.result
                i =+ 1
            return -1
    
    def run(self):
        """Reacts if nothing occurs"""
        if (len(self.options)==0):
            self.result = self.query
            return 1
            #call changes to players stats
        return -1
    
    def drawEvents(self, screen):
        """Draws the event"""
        b = screen.get_width()/100
        c = screen.get_height()/100
        pygame.draw.rect(screen, (0, 20, 170), (3*b, 3*c, 94*b, 94*c))
        pygame.draw.rect(screen, (234, 255, 0), (4.5*b, 4.5*c, 91*b, 91*c))
        pygame.draw.rect(screen, (0, 20, 170), (5*b, 5*c, 90*b, 90*c))
        if self.result == None:
            if len(self.options)>0:
                    font = pygame.font.Font(size=24)
                    text = self.query
                    x, y = font.size(text)
                    text = font.render(text, True, (255,255,255), None)
                    screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))
                    i = 0
                    a = len(self.options)
                    buttonWidth=80/a
                    for option in self.options:
                        buttonLeft = buttonWidth*i + 10
                        buttonCentre = buttonWidth*(i+0.5) + 10
                        text = option[0]
                        x, y = font.size(text)
                        text = font.render(text, True, (0,0,0), None)
                        pygame.draw.rect(screen, (255,255,255), (buttonLeft*b, 72*c, (buttonWidth-2)*b, 16*c))
                        screen.blit(text, ((buttonCentre)*b-(x/2), 80*c))
                        i =+ 1
            else:
                font = pygame.font.Font(size=24)
                text = self.query
                x, y = font.size(text)
                text = font.render(text, True, (255,255,255), None)
                screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))
        else:
            font = pygame.font.Font(size=24)
            text = self.result
            x, y = font.size(text)
            text = font.render(text, True, (255,255,255), None)
            screen.blit(text, (screen.get_width()/2-x/2, 7.5*c))

