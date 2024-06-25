import pygame

from variables import constants, variables
from classes import stones
from game_states import battle_state, homebase_state, spellcrafting_state, mainmenu_state


class Game:

    def __init__(self):

        # main game init
        pygame.display.set_caption('Spellbound Amnesia')
        pygame.font.init()
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

        # main game variables
        self.screen = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
        self.current_state = "HomeBase"

        # core class instances created
        self.battle = battle_state.Battle(self, self.screen)
        self.main_menu = mainmenu_state.MainMenu()
        self.home_base = homebase_state.HomeBase(self, self.screen)
        self.spell_crafting = spellcrafting_state.SpellCrafting(self, self.screen)

    def run(self):
        while self.running:
            self.event_handler()
            self.update()
            self.render()
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()

    def event_handler(self):
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

    def update(self):
        match self.current_state:
            case "Battlefield":
                self.battle.update()
            case "HomeBase":
                self.home_base.update()
            case "SpellCrafting":
                self.spell_crafting.update()
            case _:
                pass

    def render(self):
        match self.current_state:
            case "Battlefield":
                self.battle.draw()
            case "HomeBase":
                self.home_base.draw()
            case "SpellCrafting":
                self.spell_crafting.draw()
            case _:
                pass

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        self.current_state = state
