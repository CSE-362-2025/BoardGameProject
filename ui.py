import pygame
import random


# Constants
WINDOW_SIZE_X = 1080
WINDOW_SIZE_Y = 720
BG_COLOR = (30, 30, 30)  # Dark gray background
FONT_COLOR = (255, 255, 255)  # White text


# Adjust this based on your UI layout (percentage based)
DICE_POS = (85, 95)
DICE_SIZE = (20, 10)
NEXT_POS = (40, 95)
MAIN1 = (15, 80)
MAIN2 = (38, 80)
MAIN3 = (62, 80)
MAIN4 = (85, 80)
MAINSIZE = (20, 20)
CARD1IN = (105, 25)
CARD1OUT = (80, 25)
CARD2IN = (105, 50)
CARD2OUT = (80, 50)
CARDSIZE = (30, 20)
PAUSE = (10, 10)
PAUSESIZE = (20, 10)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

TURN_SIZE = 80
TURN_POS = (100, 400)  # Adjust this based on your UI layout

## constants for event popup screen

# event title rect and font
EVENT_TITLE_POS_CENTRE: tuple[int] = (50, 10)
EVENT_TITLE_SIZE: tuple[int] = (80, 10)
EVENT_TITLE_FONT_SIZE: int = 50

# event description and font
EVENT_DESC_POS_CENTRE: tuple[int] = (50, 30)
EVENT_DESC_SIZE: tuple[int] = (70, 30)
EVENT_DESC_FONT_SIZE: int = 30

# button y constant for two rows
EVENT_BUTTONS_POS_Y_BOTTOM_ROW: int = 80
EVENT_BUTTONS_POS_Y_TOP_ROW: int = 50

# choice size
EVENT_BUTTONS_CHOICE_SIZE: tuple[int] = (20, 20)

# type str
EVENT_BUTTONS_CHOICE_TYPE_STR: str = "Decision Event Choice"

# mapping number of all choices -> their position tuple
# TODO: placeholder value, match all position coordinates with event popup background image
EVENT_BUTTONS_CHOICE_POS: dict[int, list[tuple]] = {
    1: [(50, EVENT_BUTTONS_POS_Y_BOTTOM_ROW)],
    2: [(30, EVENT_BUTTONS_POS_Y_BOTTOM_ROW), (80, EVENT_BUTTONS_POS_Y_BOTTOM_ROW)],
    3: [
        (20, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
        (40, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
        (60, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
    ],
    4: [
        (15, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
        (35, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
        (55, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
        (75, EVENT_BUTTONS_POS_Y_BOTTOM_ROW),
    ],
}


class UI:

    # player is current player, changes during switch_turn()
    def __init__(self, game_manager=None, player=None):
        self.game_manager = game_manager
        self.player = player
        self.screen = pygame.display.set_mode(
            (WINDOW_SIZE_X, WINDOW_SIZE_Y), pygame.RESIZABLE
        )
        self.background_img = None
        self.font = pygame.font.Font(None, 16)
        self.Buttons = [
            Button(
                DICE_POS,
                DICE_SIZE,
                "Dice",
            ),
            Button(NEXT_POS, DICE_SIZE, "Next Turn", False),
            Button(MAIN1, MAINSIZE, "New Game", False, "Resources/NEW_GAME.jpg"),
            Button(
                MAIN2, MAINSIZE, "Load Game", False, "Resources/LOAD_GAME.jpg", False
            ),
            Button(
                MAIN3,
                MAINSIZE,
                "Custom Char",
                False,
                "Resources/CUSTOM_CHARA.jpg",
                False,
            ),
            Button(MAIN4, MAINSIZE, "Settings", False, "Resources/SETTINGS.jpg", False),
            CardDisplays(
                CARD1IN,
                CARD1OUT,
                CARDSIZE,
                "Leaderboard",
            ),
            CardDisplays(CARD2IN, CARD2OUT, CARDSIZE, "Player Stats"),
            Button(PAUSE, PAUSESIZE, "Pause", True),
        ]
        self.buttonPaused = []
        self.buttonevents = []
        self.open_menus = []
        self.dice_value = 0
        self.message = None  # Variable to store the current message
        self.message_duration = 0  # Number of frames the message will stay on screen

    def update(self):
        """Updates and draws all necessary UI components."""
        board = self.game_manager.board
        players = self.game_manager.players
        # Draw the board, dice, and stats
        self.screen.fill(BG_COLOR)  # Clear screen first
        if self.background_img:
            img = pygame.transform.scale(
                pygame.image.load(self.background_img),
                (self.screen.get_width(), self.screen.get_height()),
            )
            self.screen.blit(img)
        if board:
            self.display_board(
                board, players
            )  # Call a method to draw the game board (implement as needed)
        self.display_buttons()  # Call a method to display the dice
        self.display_stats()  # Call a method to display player stats, if any
        self.display_current_turn()
        for menu in self.open_menus:
            menu.draw(self.screen)

        # If there's a message to display, show it
        if self.message_duration > 0:
            text_surface = self.font.render(self.message, True, (255, 255, 255))
            text_rect = text_surface.get_rect(bottomleft=(25, 500))
            self.screen.blit(text_surface, text_rect)
            self.message_duration -= 1

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

    def game_start(self):
        self.game_manager.start_game()
        self.return_state()

    def display_board(self, board, players):
        board.draw(self.screen, players)

    def display_stats(self):
        # Example of displaying player stats in the top-right corner
        self.font = pygame.font.Font(None, 16)
        if self.player:
            stats_text = f"{self.player.name}'s Stats: {self.player.stats}"  # You can customize this to show actual stats
            stats_surface = self.font.render(stats_text, True, FONT_COLOR)
            stats_rect = stats_surface.get_rect(
                topright=(self.screen.get_width() - 10, 10)
            )
            self.screen.blit(stats_surface, stats_rect)

    def roll_dice(self):
        self.dice_value = self.game_manager.roll_dice()  # Roll dice
        self.display_roll(self.dice_value)  # Update display after rolling
        self.game_manager.play_turn(self.dice_value)

    def display_buttons(self):
        for button in self.Buttons:
            if button.visible:
                button.display(self.screen)

    # TODO: delete this test code
    ## catch-all to force all event call
    def display_stoptile_event(self, event):
        self.display_decision_event(event)

    # Pass in event and display decision choices
    def display_decision_event(self, event):
        if event:
            self.display_message(
                f"(starting event) {event.name}: {', '.join([choice['text'] for choice in event.choices])}"
            )

            # * start the decision_event flow
            # TODO: pass decision_event backdrop image here
            self.open_menus.append(
                EventMenu(
                    "Decision Event",
                    self.game_manager.current_player,
                    image=None,
                    event=event,
                )
            )
            print("appended into `open_menus`, ending display_decision_event()")
            print(
                f"\t{event.name}: {', '.join([choice['text'] for choice in event.choices])}"
            )

    def display_computer_decision(self, event, choice_idx):
        # Display the result of the computer's decision
        self.display_message(f"Computer chose: {event.choices[choice_idx].name}")

    def display_non_decision_event(self, event):
        # Display the non-decision event
        self.display_message(f"{event.name}: {event.description}")
        self.game_manager.accept_event(event)

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
        # Example of displaying player stats in the bottom-left corner
        self.font = pygame.font.Font(None, 16)
        if self.player:
            stats_text = f"{self.player.name}'s Turn"  #
            stats_surface = self.font.render(stats_text, True, FONT_COLOR)
            stats_rect = stats_surface.get_rect(
                bottomright=(
                    0.2 * self.screen.get_width(),
                    0.9 * self.screen.get_height(),
                )
            )
            self.screen.blit(stats_surface, stats_rect)

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
                    self.buttonevents.append(result)
        for menu in self.open_menus:
            result = menu.handle_click(self.screen, pos)
            if result:
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
                        elif button.type == "Next Turn":
                            button.turn_on()
                case "Next Turn":
                    self.game_manager.switch_turn()
                    for button in self.Buttons:
                        if button.type == "Next Turn":
                            button.turn_off()
                        elif button.type == "Dice":
                            button.turn_on()
                case "New Game":
                    self.game_start()
                case "Pause":
                    self.save_state()
                    self.open_menus.append(PauseMenu("Pause"))
                case "Return":
                    self.open_menus.pop()
                    self.return_state()
                case EVENT_BUTTONS_CHOICE_TYPE_STR:
                    # one choice button has been clicked, clean up and back to menu
                    self.open_menus.pop()

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


def list_edit(list, item):
    """Removes all copies of an element from a list: helper function"""
    list = [i for i in list if i != item]
    return list


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
            Button(MAIN3, MAINSIZE, "Settings", "Resources/SETTINGS.jpg"),
            Button(MAIN4, MAINSIZE, "Quit"),
        ]


class EventMenu(Menu):

    def __draw_text_with_wrap(
        self, surface, text, color, rect, font, aa=False, bkg=None
    ) -> str:
        """Helper function that draws text and wrap it to fit the given `Rect`.
        This returns any remaining text that will not fit into the `Rect`.

        From Pygame's WiKi: https://www.pygame.org/wiki/TextWrap

        Args:
            surface (pygame.Surface): main surface
            text (str): text to display
            color (tuple[int]): color of the text
            rect (pygame.Rect): `Rect` to display text on
            font (pygame.font.Font): `Font` to use for text
            aa (bool, optional): anti-aliasing toggle. Defaults to False.
            bkg (_type_, optional): background. Defaults to None.

        Returns:
            _type_: _description_
        """
        rect = pygame.Rect(rect)
        y = rect.top
        lineSpacing = -2

        # get the height of the font
        fontHeight = font.size("Tg")[1]

        while text:
            i = 1

            # determine if the row of text will be outside our area
            if y + fontHeight > rect.bottom:
                break

            # determine maximum width of line
            while font.size(text[:i])[0] < rect.width and i < len(text):
                i += 1

            # if we've wrapped the text, then adjust the wrap to the last word
            if i < len(text):
                i = text.rfind(" ", 0, i) + 1

            # render the line and blit it to the surface
            if bkg:
                image = font.render(text[:i], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)

            surface.blit(image, (rect.left, y))
            y += fontHeight + lineSpacing

            # remove the text we just blitted
            text = text[i:]

        return text

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

    def __init__(self, name, curr_player, image=None, event=None):
        super().__init__(name, image)

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

        # * create buttons for available options

        choice_button_pos: list[tuple] = EVENT_BUTTONS_CHOICE_POS[len(event.choices)]

        for i, each_choice in enumerate(event.choices):
            # grab stat dict to compare
            curr_player_stat: dict = self.curr_player.stats
            choice_criteria_stat: dict = each_choice["criteria"]

            # check if current player can choose this choice
            is_enabled: bool = self.__is_choice_available(
                curr_player_stat, choice_criteria_stat
            )

            # create a button
            each_choice_button: Button = Button(
                centre=choice_button_pos[i],
                size=EVENT_BUTTONS_CHOICE_SIZE,
                # string to display on the button
                _type=each_choice["text"],
                enabled=is_enabled,
            )
            self.buttons.append(each_choice_button)

    def draw(self, screen):
        super().draw(screen)

        # TODO: draw pop up for title, description
        print("TODO: draw rect for event title and description")


class Button:
    """Creates a button that can track itself visually and its events"""

    def __init__(
        self, centre, size, _type: str, visible=True, image=None, enabled=True
    ):
        self.visible = visible
        self.position = centre  # Button pos is centre horizontally, base vertically(to be fixed later)
        self.size = size
        self.type: str = _type
        self.image = image
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
            button_rect = pygame.Rect(
                (self.position[0] - self.size[0] / 2) * screen_width,
                (self.position[1] - self.size[1] / 2) * screen_height,
                self.size[0] * screen_width,
                self.size[1] * screen_height,
            )
            if self.image:
                buttonimg = pygame.transform.scale(
                    pygame.image.load(self.image),
                    (self.size[0] * screen_width, self.size[1] * screen_height),
                )
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
                screen.blit(text_surface, text_rect)  # Draw the text on the screen

    def handle_click(self, screen, pos):
        if self.visible:
            if self.enabled:
                screen_width = screen.get_width() / 100
                screen_height = screen.get_height() / 100
                font = pygame.font.Font(None, 16)
                # Check if the click was inside the dice area
                button_rect = pygame.Rect(
                    (self.position[0] - self.size[0] / 2) * screen_width,
                    (self.position[1] - self.size[1] / 2) * screen_height,
                    self.size[0] * screen_width,
                    self.size[1] * screen_height,
                )
                if button_rect.collidepoint(pos):
                    return self.type


class CardDisplays(Button):
    """Used to display the clickable cards that show stats or other info"""

    def __init__(
        self, centre, centre_moved, size, type, visible=True, image=None, enabled=True
    ):
        self.main = centre
        super().__init__(centre, size, type, visible, image, enabled)
        self.moved = centre_moved
        self.hovered = False

    def display(self, screen):
        super().display(screen)

    def handle_click(self, screen, pos):
        result = super().handle_click(screen, pos)
        if result:
            if not self.hovered:
                self.position = self.moved
                self.hovered = True
            else:
                self.position = self.main
                self.hovered = False
