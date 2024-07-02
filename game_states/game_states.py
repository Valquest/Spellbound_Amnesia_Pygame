import pygame

from variables import constants
from game_states import battle_state, homebase_state, spellcrafting_state, mainmenu_state

"""
    This module manages game states. We add new game states, they event handler, updaters and drawers to have 
    transitions between game states.
    
    To add a new state, create a state instance and assign it to a variable. Then add state to each of the functions
    it needs to be added.
"""


class Game:
    """
    This is a main game state class that handles all the main game states inside of it.
    Main game initiation happens here and switching between states.
    This class handles running, updating, drawing, selecting states.
    """
    def __init__(self):

        # main game init
        pygame.display.set_caption('Spellbound Amnesia')
        pygame.font.init()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

        # main game variables
        self.screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        # starting state is set to be home
        self.current_state = "HomeBase"

        # initializing other game elements
        self.init_images()

        # core class instances created
        self.battle = battle_state.Battle(self, self.screen)
        self.main_menu = mainmenu_state.MainMenu()
        self.home_base = homebase_state.HomeBase(self, self.screen)
        self.spell_crafting = spellcrafting_state.SpellCrafting(self, self.screen)

    def run(self) -> None:
        """
        Runs all the other functions needed for a pygame visual management.
        :return: None
        """
        while self.running:
            self.event_handler()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def event_handler(self) -> None:
        """
        Manages event handling functionality for the game states
        :return: None
        """
        # poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            match self.current_state:
                case "Battlefield":
                    self.battle.handle_event(event)
                case "HomeBase":
                    self.home_base.handle_event(event)
                case "SpellCrafting":
                    self.spell_crafting.handle_event(event)
                case _:
                    pass

    def update(self) -> None:
        """
        Runs state method that update states variables, visuals etc.
        :return: None
        """
        match self.current_state:
            case "Battlefield":
                self.battle.update()
            case "HomeBase":
                self.home_base.update()
            case "SpellCrafting":
                self.spell_crafting.update()
            case _:
                pass

    def render(self) -> None:
        """
        Runs state method that renders visual information.
        :return: None
        """
        match self.current_state:
            case "Battlefield":
                self.battle.draw()
            case "HomeBase":
                self.home_base.draw()
            case "SpellCrafting":
                self.spell_crafting.draw()
            case _:
                pass

    def get_state(self) -> str:
        """
        Gets current state and returns it.
        :return: String value of a current state.
        """
        return self.current_state

    def set_state(self, state) -> None:
        """
        Sets main game state.
        :param state: State name entered as a string.
        :return: None
        """
        self.current_state = state

    def init_images(self) -> None:
        from classes import stones
        # Load the shared image once Pygame is initialized
        try:
            stones.MagicStone.shared_image = pygame.image.load(
                stones.MagicStone.image_path).convert_alpha()
            print(f"Image loaded successfully: {stones.MagicStone.image_path}")
        except pygame.error as e:
            print(f"Failed to load image: {e}")