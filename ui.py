import pygame
import random


# Constants
WINDOW_SIZE_X = 1080
WINDOW_SIZE_Y = 720
BG_COLOR = (30, 30, 30)  # Dark gray background
FONT_COLOR = (255, 255, 255)  # White text


# Adjust this based on your UI layout (percentage based)
DICE_POS = (88, 88)
DICE_SIZE = (20, 15)
MAIN1 = (15, 70)
MAIN2 = (38, 70)
MAIN3 = (62, 70)
MAIN4 = (85, 70)
MAINSIZE = (20, 12)
CARD1IN = (115, 17.5)
CARD1OUT = (90, 17.5)
CARD2IN = (115, 32.5)
CARD2OUT = (90, 32.5)
CARDSIZE = (30, 20)
PAUSE = (5, 2.5)
PAUSESIZE = (10, 5)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TURN_SIZE = 80
TURN_POS = (100, 400)  # Adjust this based on your UI layout

## constants for event popup screen

# Rect with TSS background
EVENT_RECT_POS_CENTRE: tuple[int] = (50, 50)
EVENT_RECT_SIZE: tuple[int] = (80, 80)
EVENT_RECT_TSS_PATH: str = "Resources/tss.jpg"

# margin for left/right in percentage
EVENT_LR_MARGIN: int = 3
# margin for top/bottom in percentage
EVENT_TB_MARGIN: int = 2

# event title rect and font
EVENT_TITLE_FONT_SIZE: int = 40
EVENT_FONT_COLOUR: tuple[int] = (96, 35, 58)

# event description and font
EVENT_DESC_FONT_SIZE: int = 25

# event button text size
EVENT_BUTTONS_FONT_SIZE: int = 22

# event button colours
EVENT_BUTTONS_BORDER_COLOUR: tuple[int] = (94, 36, 51)
EVENT_BUTTONS_FILL_ENABLED_COLOUR: tuple[int] = (182, 133, 129)
EVENT_BUTTONS_FILL_DISABLED_COLOUR: tuple[int] = (90, 66, 63)

# choice size
EVENT_BUTTONS_CHOICE_SIZE: tuple[int] = (17, 10)


def draw_text_with_wrap_centery(
    surface, text, color, rect, font, aa=True, bkg=None
) -> str:
    """Helper function that draws text and wrap it to fit the given `Rect`.
    This returns any remaining text that will not fit into the `Rect`.
    This will force all text to have the same `centery` as the given `rect`,
    only use for short texts.

    Derived from Pygame's WiKi: https://www.pygame.org/wiki/TextWrap

    Args:
        surface (pygame.Surface): main surface
        text (str): text to display
        color (tuple[int]): color of the text
        rect (pygame.Rect): `Rect` to display text on
        font (pygame.font.Font): `Font` to use for text
        aa (bool, optional): anti-aliasing toggle. Defaults to True.
        bkg (_type_, optional): background. Defaults to None.

    Returns:
        str: left over string that could not fit into given rect
    """
    rect = pygame.Rect(rect)
    y = rect.top
    line_spacing = 2

    # get the height of the font
    font_height = font.size("Tg")[1]

    # padding for L/R
    padding = surface.get_width() / 100 * 3

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width - padding and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], True, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        text_rect = image.get_rect(center=rect.center)
        text_rect.centery = rect.centery
        surface.blit(image, text_rect)
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text


def draw_text_with_wrap_centery_increment(
    surface, text, color, rect, font, aa=True, bkg=None, is_dry_run=False
) -> str:
    """Helper function that draws text and wrap it to fit the given `Rect`.
    This returns any remaining text that will not fit into the `Rect`.
    Text rect's will start from given rect's top and will draw until the bottom,
    incrementing y value.

    Derived from Pygame's WiKi: https://www.pygame.org/wiki/TextWrap

    Args:
        surface (pygame.Surface): main surface
        text (str): text to display
        color (tuple[int]): color of the text
        rect (pygame.Rect): `Rect` to display text on
        font (pygame.font.Font): `Font` to use for text
        aa (bool, optional): anti-aliasing toggle. Defaults to True.
        bkg (_type_, optional): background. Defaults to None.
        is_dry_run (bool, optional): if set, won't render. Defaults to False.

    Returns:
        str: left over string that could not fit into given rect
    """

    # padding for L/R
    padding_lr = surface.get_width() / 100 * 1

    # padding for top/bottom
    padding_tb = surface.get_height() / 100 * 2.5
    rect = pygame.Rect(rect)

    y = rect.top + padding_tb
    line_spacing = 2

    # get the height of the font
    font_height = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + font_height > rect.bottom + padding_tb:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width - padding_lr and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text):
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], True, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        text_rect = image.get_rect(center=rect.center)
        text_rect.centery = y
        if not is_dry_run:
            surface.blit(image, text_rect)
        y += font_height + line_spacing

        # remove the text we just blitted
        text = text[i:]

    return text


class UI:

    # player is current player, changes during switch_turn()
    def __init__(self, game_manager=None, player=None):
        self.game_manager = game_manager
        self.player = player
        self.screen = pygame.display.set_mode(
            (WINDOW_SIZE_X, WINDOW_SIZE_Y), pygame.RESIZABLE
        )
        self.width = self.screen.get_width()
        self.backgrounds = dict(
            title="Resources/Title_Screen.png", wood="Resources/background_wood.png", year1="Resources/board_year1.png",
        )
        self.curr_background = self.backgrounds["title"]
        self.background_img = pygame.transform.scale(
            pygame.image.load(self.curr_background),
            (self.screen.get_width(), self.screen.get_width() * (41 / 59)),
        )
        self.font = pygame.font.Font(None, 16)
        self.Buttons = [
            Button(DICE_POS, DICE_SIZE, "Dice", image="Resources/Dice.png"),
            Button(DICE_POS, DICE_SIZE, "Next Turn", False),
            Button(MAIN1, MAINSIZE, "New Game", False, "Resources/NEW_GAME.jpg"),
            Button(MAIN2, MAINSIZE, "Load Game", False, "Resources/LOAD_GAME.jpg", False),
            Button(MAIN3,MAINSIZE,"Custom Char",False,"Resources/CUSTOM_CHARA.jpg",False,),
            Button(MAIN4, MAINSIZE, "Settings", False, "Resources/SETTINGS.jpg", False),
            Button(PAUSE, PAUSESIZE, "Pause", True),]
        self.Buttons.insert(0,CardDisplays(CARD1IN,CARD1OUT,CARDSIZE,"Player Stats",image="Resources/rmc_card.png",),)
        self.Buttons.insert(1,CardDisplays(CARD2IN,CARD2OUT,CARDSIZE,"Leaderboard",image="Resources/rmc_card.png",),)
        self.buttonPaused = []
        self.buttonevents = []
        self.open_menus = []
        self.dice_value = 0
        self.message = None  # Variable to store the current message
        self.message_duration = 0  # Number of frames the message will stay on screen
        self.sounds = dict(click=pygame.mixer.Sound("Resources/sounds/click.ogg"),
                           start=pygame.mixer.Sound("Resources/sounds/I am notta da mario.ogg"),
                           pause=pygame.mixer.Sound("Resources/sounds/paused.ogg"),
                           athletic=pygame.mixer.Sound("Resources/sounds/Athletics.ogg"),
                           english=pygame.mixer.Sound("Resources/sounds/Bilingualism(English).ogg"),
                           french=pygame.mixer.Sound("Resources/sounds/Bilingualism(French).ogg"),
                           military=pygame.mixer.Sound("Resources/sounds/Military.ogg"),
                           social=pygame.mixer.Sound("Resources/sounds/Socials.ogg"),
                           academic=pygame.mixer.Sound("Resources/sounds/Academics.ogg"))
        self.sounds['click'].set_volume(0.5)
        self.track = 0
        self.year = 0


    def update(self):
        """Updates the screen"""
        board = self.game_manager.board
        players = self.game_manager.players
        """Updates and draws all necessary UI components."""
        # Draw the board, dice, and stats, starting by filling the background with either an image or colour
        if self.background_img:
            if self.width != self.screen.get_width():
                self.width = self.screen.get_width()
                self.background_img = pygame.transform.scale(
                    pygame.image.load(self.curr_background),
                    (self.screen.get_width(), self.screen.get_width() * (41 / 59)),
                )
            self.screen.blit(self.background_img, (0, 0))
        else:
            self.screen.fill(BG_COLOR)
        if board:
            self.display_board(board, players)  # Call a method to draw the game board

        # If there's a message to display, show it
        if self.message_duration > 0:
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.screen.get_width()/2, self.screen.get_width()*(41/150)))
            self.screen.blit(text_surface, text_rect)
            self.message_duration -= 1

        self.display_buttons()  # Call a method to display the dice
        self.display_current_turn()
        self.display_leaderboard()
        for menu in self.open_menus:
            menu.draw(self.screen)
        if not pygame.mixer.music.get_busy():
            self.set_sound()

    def main_menu(self):
        self.save_state()
        for button in self.Buttons:
            if (
                button.type == "New Game"
                or button.type == "Load Game"
                or button.type == "Custom Char"
                or button.type == "Settings"
            ):
                button.turn_on()

    def set_sound(self):
            if self.player:
                pygame.mixer.music.load("Resources/sounds/Relaxation.ogg")
                pygame.mixer.music.play()
                match self.track:
                    case 0:
                        pygame.mixer.music.queue("Resources/sounds/Precision(Midgame).ogg")
                    case 1:
                        pass
                    case 2:
                        pygame.mixer.music.queue("Resources/sounds/Precision(Midgame).ogg")
                    case 3:
                        pygame.mixer.music.queue("Resources/sounds/Music Box.ogg")
                    case _:
                        pygame.mixer.music.queue("Resources/sounds/Precision(Midgame).ogg")
                        print("Track Reset")
                        self.track=0
                self.track =+ 1
            else:
                pygame.mixer.music.load("Resources/sounds/Precision(Title).ogg")
                pygame.mixer.music.play()

    def game_start(self):
        self.game_manager.start_game()
        self.set_sound()
        self.curr_background = self.backgrounds["wood"]
        self.width = 1
        self.return_state()

    def display_board(self, board, players):
        self.year = self.game_manager.year
        match self.year:
            case 0:
                if self.curr_background != self.backgrounds["year1"]:
                    self.curr_background = self.backgrounds["year1"]
                    self.width=1
            case _:
                self.curr_background = self.backgrounds["wood"]
        board.draw(self.screen, players)

    def roll_dice(self):
        self.dice_value = self.game_manager.roll_dice()  # Roll dice
        self.display_roll(self.dice_value)  # Update display after rolling
        self.game_manager.play_turn(self.dice_value)

    def display_buttons(self):
        for button in self.Buttons:
            if button.visible:
                button.display(self.screen)

    # Pass in event and display decision choices
    def display_decision_event(self, event):
        if event:
            # * start the decision_event flow
            self.save_state()
            self.open_menus.append(
                EventMenu(
                    "Decision Event",
                    self.game_manager.current_player,
                    image="Resources/tss.jpg",
                    event=event,
                    game_manager=self.game_manager
                )
            )


    def display_computer_decision(self, event, choice_idx):
        # Display the result of the computer's decision
        self.display_message(f"Computer chose: {event.choices[choice_idx].name}")

    def display_non_decision_event(self, event):
        # Display the non-decision event
        self.display_message(f"{event[0]}: {event[1]}")
        for button in self.Buttons:
            if button.type == "Next Turn":
                button.turn_on()

    def display_computer_non_decision_event(self, event):
        # Display the result of the computer's non-decision event
        self.display_message(f"Computer: {event.name} | Result: {event.result}")
        self.game_manager.accept_event(event)

    # Display game messages such as player turn, etc.
    def display_message(self, message, duration=200):
        # Set background color for the message area (optional)
        self.message = message
        self.message_duration = duration

    def display_current_turn(self):
        # Displays player stats
        self.font = pygame.font.Font(None, 16)
        if self.player:
            portrait = self.player.get_portrait()
            info = (self.player.name, self.player.stats, portrait)
            self.Buttons[0].update_info(info)
            if portrait:
                if self.screen.get_width() / 1.75 < self.screen.get_height():
                    width = self.screen.get_width() / 100
                else:
                    width = self.screen.get_height() / 60
                portrait = pygame.transform.rotate(portrait, 16)
                portrait = pygame.transform.scale(portrait, (width * 28, width * 28))
                portrait_rect = portrait.get_rect(
                    bottomleft=(0 - 40, self.screen.get_height() + 30)
                )
                self.screen.blit(portrait, portrait_rect)
            playerlist = self.game_manager.players
            for player in range(len(playerlist)):
                if self.player == playerlist[player]:
                    start = player
                    break
            move_over = 0
            for player in range(len(playerlist)-1):
                start += 1
                move_over += 1
                if start >= len(playerlist):
                    start = 0
                image = pygame.transform.scale(playerlist[start].next_up, (width * 8, width * 10))
                image_rect = image.get_rect(
                    bottomleft=(((35 - (move_over*5))*self.screen.get_width()/100), self.screen.get_height() - 10)
                )
                self.screen.blit(image, image_rect)



    def display_leaderboard(self):
        self.font = pygame.font.Font(None, 16)
        if self.player:
            playerlist={}
            for player in self.game_manager.players:
                playerlist.update({player.name:random.randint(1,10)})
            info = ("Leaderboard", playerlist, pygame.image.load("Resources/test_meeple.png"))
            self.Buttons[1].update_info(info)

    def change_current_player(self, player):
        self.player = player
        # self.display_message(f"{player.name}'s turn")

    def display_roll(self, roll):
        # Display the roll value
        self.display_message(f"Rolled: {roll}")

    def handle_click(self, pos):
        for button in self.Buttons:
            if button.visible:
                result = button.handle_click(self.screen, pos)
                if result:
                    self.sounds["click"].play()
                    self.buttonevents.append(result)
        for menu in self.open_menus:
            result = menu.handle_click(self.screen, pos)
            if result:
                self.sounds["click"].play()
                self.buttonevents.append(result)

    def run(self):
        """React to events in the list FIFO, and remove all following copies of that event - Should probably move to events"""
        if len(self.buttonevents) > 0:
            next_event = self.buttonevents[0]
            self.buttonevents = list_edit(self.buttonevents, next_event)
            print(next_event)
            match next_event:
                case "Dice":
                    self.roll_dice()
                    for button in self.Buttons:
                        if button.type == "Dice":
                            button.turn_off()
                case "Next Turn":
                    self.game_manager.switch_turn()
                    for button in self.Buttons:
                        if button.type == "Next Turn":
                            button.turn_off()
                        elif button.type == "Dice":
                            button.turn_on()
                case "New Game":
                    self.sounds["start"].play()
                    self.game_start()
                case "Save":
                    random.choice(list(self.sounds.values())).play()
                case "Pause":
                    self.sounds["pause"].play()
                    self.save_state()
                    self.open_menus.append(PauseMenu("Pause"))
                case "Return":
                    self.open_menus.pop()
                    self.return_state()
                case "choice":
                    # one choice button has been clicked, clean up and back to menu
                    self.open_menus.pop()
                    self.return_state()
                    self.game_manager.switch_turn()
                case "Quit":
                    pygame.event.Event(quit)
        if self.game_manager.is_game_over():
            self.player=None


    def save_state(self):
        for button in self.Buttons:
            if button.visible:
                self.buttonPaused.append(button)
                button.turn_off()

    def return_state(self):
        for button in self.Buttons:
            if button.visible:
                button.turn_off()
        for button in self.buttonPaused:
            button.turn_on()
        self.buttonPaused = []


def list_edit(target_list, item):
    """Removes all copies of an element from a list: helper function"""
    ret = [i for i in target_list if i != item]
    return ret


class Menu:

    def __init__(self, name, image=None):
        self.name = name
        self.image = image
        self.buttons = []

    def draw(self, screen):
        menu_background = pygame.Surface((screen.get_width(), screen.get_height()))
        menu_background.fill((0, 0, 0))
        menu_background.set_alpha(160)
        screen.blit(menu_background, (0, 0))
        for button in self.buttons:
            button.display(screen)

    def handle_click(self, screen, pos):
        for button in self.buttons:
            result = button.handle_click(screen, pos)
            if result:
                return result


class PauseMenu(Menu):
    def __init__(self, name, image=None):
        super().__init__(name, image)
        self.buttons = [
            Button(MAIN1, MAINSIZE, "Return"),
            Button(MAIN2, MAINSIZE, "Save"),
            Button(MAIN3, MAINSIZE, "Settings", image="Resources/SETTINGS.jpg"),
            Button(MAIN4, MAINSIZE, "Quit"),
        ]


class EventMenu(Menu):

    def __is_choice_available(self, player_stat: dict, choice_stat: dict) -> bool:
        """Check if the `player_stat` is higher or equal than `choice_stat` dictionary.
        This assumes two given dict has the same keys.

        Args:
            player_stat (dict): stat dict for current player
            choice_stat (dict): required stat level to be able to choose this action

        Returns:
            bool: True if player can check this event
        """
        for each_key in list(player_stat.keys()):
            if player_stat[each_key] < choice_stat[each_key]:
                # player does not meet the required criteria
                return False
        return True

    def __init__(self, name, curr_player, game_manager, image=None, event=None):
        super().__init__(name, image)

        self.game_manager = game_manager

        if event is None:
            raise RuntimeError("EventMenu(): the received `event` is None")

        self.image: str | None = image
        if image is None:
            # TODO: replace/remove this fallback image path
            # fall back to testing default image
            self.image = "Resources/gunsalute-scarlets-mckenzie.jpg"

        self.curr_player = curr_player
        self.event = event
        self.buttons: list[Button] = []
        self.tss = pygame.image.load(EVENT_RECT_TSS_PATH)
        self.event_image = pygame.image.load("Resources/gunsalute-scarlets-mckenzie.jpg")

    def __get_font_size_to_fit_all(self, screen: pygame.Surface, rect: pygame.Rect, text: str, colour: tuple[int], initial_font_size: int, font_family: str = None) -> int:
        """Find a font size that fits all of given string into the rect.

        This finds the font size that can fit all given text and returns
        the font size. This will render the font on the given rect.
        Currently, font-size decrements by 1.

        Args:
            screen (pygame.Surface): the base surface
            rect (pygame.Rect): rect obj to fit text in
            text (str): text to render
            colour (tuple[int]): colour of the text
            initial_font_size (int): Initial font size to use
            font_family (str, optional): path to specific font to use. Defaults to None.

        Returns:
            int: font size value found

        """
        step_size: int = 1
        curr_font_size = initial_font_size
        while True:
            each_font: pygame.font.Font = pygame.font.Font(font_family, curr_font_size)
            # try to draw text
            remaining: str = draw_text_with_wrap_centery_increment(
                screen,
                text,
                colour,
                rect,
                each_font,
                is_dry_run=True
            )
            if len(remaining) == 0:
                break

            curr_font_size -= step_size

        return curr_font_size

    def draw(self, screen):
        super().draw(screen)

        # DRY
        screen_width = screen.get_width() / 100
        screen_height = screen.get_height() / 100

        # * event popup rect with `TSS` containing title and desc
        event_rect_left = (
            EVENT_RECT_POS_CENTRE[0] - EVENT_RECT_SIZE[0] / 2
        ) * screen_width
        event_rect_top = (
            EVENT_RECT_POS_CENTRE[1] - EVENT_RECT_SIZE[1] / 2
        ) * screen_height
        event_rect_width = EVENT_RECT_SIZE[0] * screen_width
        event_rect_height = screen.get_height()

        event_rect: pygame.Rect = pygame.Rect(
            event_rect_left, event_rect_top, event_rect_width, event_rect_height
        )

        # load TSS image
        tss = self.tss
        tss.convert()
        tss_rect: pygame.Rect = tss.get_rect()

        # fit TSS into event_rect
        tss_rect_adjusted: pygame.Rect = tss_rect.fit(event_rect)
        tss_resized = pygame.transform.scale(tss, tss_rect_adjusted.size)

        # prep event title
        event_title_font: pygame.font.Font = pygame.font.Font(
            "Resources/fonts/franklin_gothic_book_italic.ttf", EVENT_TITLE_FONT_SIZE
        )
        # title rect with padding
        event_title_rect: pygame.Rect = pygame.Rect(
            0,
            0,
            tss_rect_adjusted.width,
            # TODO: set height such that the longest event title can fit
            15 * screen_height,
        )
        event_title_rect.centerx = tss_rect_adjusted.centerx
        event_title_rect.top = tss_rect_adjusted.top + 10 * screen_height

        # prep event description box, right half below the title box
        event_desc_rect: pygame.Rect = pygame.Rect(
            0,
            0,
            tss_rect_adjusted.width // 2,
            28 * screen_height,
        )
        event_desc_rect.topleft = (
            (event_title_rect.bottomleft[0] + event_title_rect.bottomright[0]) / 2,
            event_title_rect.bottom,
        )
        event_desc_rect.top = event_title_rect.bottom
        # move to the left of the screen
        event_desc_rect.left -= screen.get_width() / 100 * 0.5

        # prep box for image insert
        event_img_rect: pygame.Rect = pygame.Rect(
            0, 0, tss_rect_adjusted.width // 2, 25 * screen_height
        )
        # move image box to the left of the desc box
        event_img_rect.topleft = event_title_rect.bottomleft
        # move to the right for 0.2% of the screen
        event_img_rect.left += screen.get_width() / 100 * 0.2
        # TODO: replace this with a pool of event desc images
        event_img = self.event_image
        event_img.convert()
        # fit this image into img_rect
        event_img_fit = event_img.get_rect().fit(event_img_rect)
        event_img_resized = pygame.transform.scale(event_img, event_img_fit.size)

        # top value for first button (desc box + margin)
        ecb_top = event_desc_rect.bottom + screen_height * 0.5

        # grab width for each button based on TSS rect's width
        ecb_width = tss_rect_adjusted.width - EVENT_LR_MARGIN * screen_width

        # calculate left for all ECB's
        ecb_left = tss_rect_adjusted.left + EVENT_LR_MARGIN * screen_width

        # reset every frame
        self.buttons: list[EventChoiceButton] = []
        for i, each_choice in enumerate(self.event.choices):
            # grab stat dict to compare
            curr_player_stat: dict = self.curr_player.stats
            choice_criteria_stat: dict = each_choice["criteria"]

            # check if current player can choose this choice
            is_enabled: bool = self.__is_choice_available(
                curr_player_stat, choice_criteria_stat
            )

            # increment top (ecb_top + ECB's height + margin)
            current_ecb_top = ecb_top + (
                +EVENT_BUTTONS_CHOICE_SIZE[1] * screen_height + screen_height * 1
            ) * int(i)

            # calculate bottom for current button: current_ecb_top + ECB's height
            current_ecb_bottom = (
                current_ecb_top + EVENT_BUTTONS_CHOICE_SIZE[1] * screen_height
            )

            # create EventChoiceButton
            each_choice_button: Button = EventChoiceButton(
                centerx=event_title_rect.centerx,
                height=EVENT_BUTTONS_CHOICE_SIZE[1] * screen_height,
                top=current_ecb_top,
                left=ecb_left,
                bottom=current_ecb_bottom,
                width=ecb_width,
                button_text=each_choice["text"],
                event=self.event,
                choice_idx=i,
                curr_player=self.curr_player,
                centre=None,
                size=EVENT_BUTTONS_CHOICE_SIZE,
                # string to display on the button
                _type="choice",
                enabled=is_enabled,
                game_manager=self.game_manager
            )
            self.buttons.append(each_choice_button)

        # * ALL draw events

        # resized TSS image rect
        screen.blit(tss_resized, tss_rect_adjusted)

        # border for event desc rect (TSS colour)
        pygame.draw.rect(screen, EVENT_BUTTONS_BORDER_COLOUR, event_desc_rect, 3)

        # draw title on top
        draw_text_with_wrap_centery_increment(
            screen,
            str(self.event.name),
            EVENT_FONT_COLOUR,
            event_title_rect,
            event_title_font,
        )

        # draw desc on top
        fitting_font_size: int = self.__get_font_size_to_fit_all(
            screen,
            event_desc_rect,
            str(self.event.description),
            EVENT_FONT_COLOUR,
            EVENT_DESC_FONT_SIZE,
            font_family="Resources/fonts/news_gothic_std_medium.otf"
        )
        event_desc_font: pygame.font.Font = pygame.font.Font(
            "Resources/fonts/news_gothic_std_medium.otf", fitting_font_size
        )
        draw_text_with_wrap_centery_increment(
            screen,
            str(self.event.description),
            EVENT_FONT_COLOUR,
            event_desc_rect,
            event_desc_font,
        )

        # draw desc image
        screen.blit(event_img_resized, event_img_fit)

        # ensure buttons are drawn over menu
        for each_button in self.buttons:
            each_button.display(screen)


class Button(object):
    """Creates a button that can track itself visually and its events"""

    def __init__(
        self, centre, size, _type: str, visible=True, image=None, enabled=True
    ):
        self.visible = visible
        self.position = centre  # Button pos is centre horizontally, base vertically(to be fixed later)
        self.size = size
        self.type: str = _type
        if image:
            self.image = pygame.image.load(image)
        else:
            self.image = None
        self.enabled = enabled

    def turn_on(self):
        self.visible = True

    def turn_off(self):
        self.visible = False

    def display(self, screen):
        if self.visible:
            screen_width = screen.get_width() / 100
            screen_height = screen.get_height() / 100
            font = pygame.font.Font(None, 16)
            # Draw dice background (square)
            if self.image:
                if screen_width / 2 < screen_height:
                    button_rect = pygame.Rect(
                        (self.position[0] - self.size[0] / 2) * screen_width,
                        (
                            self.position[1] * screen_height
                            - (self.size[1] / 2) * screen_width
                        ),
                        self.size[0] * screen_width,
                        self.size[1] * screen_width,
                    )
                    screen_height = screen_width
                else:
                    button_rect = pygame.Rect(
                        self.position[0] * screen_width
                        - (self.size[0] * screen_height),
                        self.position[1] * screen_height
                        - (self.size[1] * screen_height),
                        self.size[0] * 2 * screen_height,
                        self.size[1] * 2 * screen_height,
                    )
                    screen_height = screen_height * 2
                    screen_width = screen_height
                buttonimg = pygame.transform.scale(self.image,(self.size[0] * screen_width, self.size[1] * screen_height),)
                if not self.enabled:
                    buttonimg.set_alpha(160)
                screen.blit(buttonimg, button_rect)
            else:
                button_rect = pygame.Rect(
                    (self.position[0] - self.size[0] / 2) * screen_width,
                    (self.position[1] - self.size[1] / 2) * screen_height,
                    self.size[0] * screen_width,
                    self.size[1] * screen_height,
                )
                if self.enabled:
                    pygame.draw.rect(
                        screen, WHITE, button_rect
                    )  # Background of the button
                pygame.draw.rect(screen, BLACK, button_rect, 3)  # Border for the button
                # Draw value (centered in the square)
                text_surface = font.render(str(self.type), True, BLACK)
                text_rect = text_surface.get_rect(
                    center=button_rect.center
                )  # Center the text inside the dice square
                screen.blit(text_surface, text_rect)  # Draw the text on the screen

    def handle_click(self, screen, pos):
        if self.visible:
            if self.enabled:
                screen_width = screen.get_width() / 100
                screen_height = screen.get_height() / 100
                # Check if the click was inside the dice area

                if self.image:
                    if screen_width / 2 < screen_height:
                        button_rect = pygame.Rect(
                            (self.position[0] - self.size[0] / 2) * screen_width,
                            (
                                self.position[1] * screen_height
                                - (self.size[1] / 2) * screen_width
                            ),
                            self.size[0] * screen_width,
                            self.size[1] * screen_width,
                        )
                    else:
                        button_rect = pygame.Rect(
                            self.position[0] * screen_width
                            - (self.size[0] * screen_height),
                            self.position[1] * screen_height
                            - (self.size[1] * screen_height),
                            self.size[0] * 2 * screen_height,
                            self.size[1] * 2 * screen_height,
                        )
                else:
                    button_rect = pygame.Rect(
                        (self.position[0] - self.size[0] / 2) * screen_width,
                        (self.position[1] - self.size[1] / 2) * screen_height,
                        self.size[0] * screen_width,
                        self.size[1] * screen_height,
                    )
                if button_rect.collidepoint(pos):
                    return self.type


class EventChoiceButton(Button):

    def __init__(
        self,
        centerx: int,
        height: int,
        top: int,
        left: int,
        bottom: int,
        width: int,
        button_text: str,
        choice_idx: int,
        event,
        curr_player,
        game_manager,
        *args,
        **kwargs,
    ):
        # to dynamically draw buttons rather than constant percentage
        self.centerx = centerx
        self.height = height
        self.top = top
        self.left = left
        self.bottom = bottom
        self.width = width

        # tmp fix
        self.game_manager = game_manager

        # set center for parent's class
        self.center = (centerx, self.top + self.height / 2)

        self.button_text = button_text
        self.choice_idx: int = choice_idx
        self.event = event
        self.curr_player = curr_player
        super().__init__(*args, **kwargs)

    def display(self, screen):
        """Overridden, display button with choice-button-style.
        Draw TSS backdrop with texts (title, description) first, then choice buttons.

        Args:
            screen (Surface): main game screen
        """

        if not self.visible:
            # not visible, skip
            return

        # ! DRY
        screen_width = screen.get_width() / 100
        screen_height = screen.get_height() / 100

        button_font = pygame.font.Font(None, EVENT_BUTTONS_FONT_SIZE)

        button_rect = pygame.rect.Rect(
            self.left,
            self.top,
            self.width,
            self.size[1] * screen_height,
        )

        # adjust rect with given value
        button_rect.width = self.width
        button_rect.top = self.top
        button_rect.bottom = self.bottom
        button_rect.centerx = self.centerx

        # draw button rect on screen
        fill_colour = (
            EVENT_BUTTONS_FILL_ENABLED_COLOUR
            if self.enabled
            else EVENT_BUTTONS_FILL_DISABLED_COLOUR
        )

        # fill
        pygame.draw.rect(screen, fill_colour, button_rect)
        # border
        pygame.draw.rect(screen, EVENT_BUTTONS_BORDER_COLOUR, button_rect, 3)

        # draw text on top
        draw_text_with_wrap_centery_increment(
            screen, self.button_text, EVENT_FONT_COLOUR, button_rect, button_font
        )

    def handle_click(self, screen, pos) -> str | None:
        """Handle click for each EventChoiceButton, and return str literal
        for `UI` to handle cleanup.

        Args:
            screen (Surface): main screen
            pos (tuple[int]): mouse click event position

        Returns:
            str: str literal, if clicked. None otherwise.
        """

        # ECB handle click
        button_rect = pygame.rect.Rect(
            self.left,
            self.top,
            self.width,
            self.size[1] * screen.get_height() / 100,
        )

        # adjust rect with given value
        button_rect.width = self.width
        button_rect.top = self.top
        button_rect.bottom = self.bottom
        button_rect.centerx = self.centerx

        if button_rect.collidepoint(pos):
            # ! TBD
            print(f"applying result for id={self.choice_idx}; text={self.button_text}")
            print(f"\tbefore: {self.curr_player.stats}")

            # apply the consequence
            self.game_manager.event_choice(self.event, self.choice_idx)

            # ! TBD
            print(f"\tafter: {self.curr_player.stats}")
            return "choice"
        return None


class CardDisplays(Button):
    """Used to display the clickable cards that show stats or other info"""

    def __init__(
        self, centre, centre_moved, size, type, visible=True, image=None, enabled=True
    ):
        self.main = centre
        super().__init__(centre, size, type, visible, image, enabled)
        self.moved = centre_moved
        self.hovered = False
        self.info = None

    def display(self, screen):
        if self.visible:
            screen_width = screen.get_width() / 100
            screen_height = screen_width
            w = 21
            h = 14
            font = pygame.font.Font(None, 16)
            # Draw dice background (square)
            button_rect = pygame.Rect(
                (self.position[0] - w) * screen_width,
                (self.position[1] - h) * screen_height,
                w * screen_width,
                h * screen_height,
            )
            if self.image:
                if screen_width / 1.75 < screen_height:
                    screen_height = screen_width
                else:
                    screen_width = screen_height
                buttonimg = pygame.transform.scale(self.image, (w * screen_width, h * screen_height))
                buttonimg = self.add_stats(buttonimg.copy())
                if not self.enabled:
                    buttonimg.set_alpha(160)
                screen.blit(buttonimg, button_rect)
            else:
                if self.enabled:
                    pygame.draw.rect(
                        screen, WHITE, button_rect
                    )  # Background of the button
                pygame.draw.rect(screen, BLACK, button_rect, 3)  # Border for the button
                # Draw value (centered in the square)
                text_surface = font.render(str(self.type), True, BLACK)
                text_rect = text_surface.get_rect(
                    center=button_rect.center
                )  # Center the text inside the dice square
                text_surface = self.add_stats(text_surface, text_rect)
                screen.blit(text_surface, text_rect)  # Draw the text on the screen

    def add_stats(self, buttonimg):
        if self.info:
            width = buttonimg.get_width() / 100
            height = buttonimg.get_height() / 100
            font = pygame.font.Font(None, int(height * 8))
            name = font.render(str(self.info[0]), False, WHITE)
            buttonimg.blit(name, (30 * width, 25.5 * height))
            base = 40
            for item in self.info[1]:
                stat = font.render(str(item), True, BLACK)
                val = font.render(str(self.info[1][item]), True, BLACK)
                buttonimg.blit(stat, (60 * width, base * height))
                buttonimg.blit(val, (85 * width, base * height))
                base = base + 10
            portrait = pygame.transform.scale(self.info[2], (width * 50, width * 50))
            portrait_rect = portrait.get_rect(
                bottomleft=(0 - width + 10, (height * 100) - width + 5)
            )
            buttonimg.blit(portrait, portrait_rect)
        return buttonimg

    def update_info(self, info):
        self.info = info

    def handle_click(self, screen, pos):
        if self.visible:
            if self.enabled:
                screen_width = screen.get_width() / 100
                screen_height = screen_width
                w = 21
                h = 14
                font = pygame.font.Font(None, 16)
                # Check if the click was inside the dice area
                button_rect = pygame.Rect(
                    (self.position[0] - w) * screen_width,
                    (self.position[1] - h) * screen_height,
                    w * screen_width,
                    h * screen_height,
                )
                if button_rect.collidepoint(pos):
                    if not self.hovered:
                        self.position = self.moved
                        self.hovered = True
                    else:
                        self.position = self.main
                        self.hovered = False
                    return self.type
