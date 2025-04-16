import pygame
from core.state.appstate import APPSTATE
from sys import exit as ex
from ui.menus.menu import Menu
from core.game.game import Game
from core.sound.sound import SoundManager
from util.debug import DebugMenu

class Window():
    def __init__(self, version, state_manager):
        pygame.init()
        pygame.font.init()
        self.state = state_manager
        self.width = 1000
        self.height = 800
        self.version = version
        self.title = f"Distant Worlds - {self.version}"
        pygame.display.set_caption(self.title)
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.state,self)  # Menu also shares the same state manager
        self.sound = SoundManager()
        self.debug = DebugMenu(self.screen,self,None)

    def main_loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F9:
                        print("loading debug menu...")
                        self.debug.toggle()
            self.sound.play_music("menu")
            if self.debug.on:
                self.debug.update(None)
            if self.state.is_app_state(APPSTATE.MAIN_MENU):
                self.menu.render_main()
            elif self.state.is_app_state(APPSTATE.GAME_ACTIVE):
                self.sound.stop_music()
                self.start_game()
            elif self.state.is_app_state(APPSTATE.OPTIONS_MENU):
                self.menu.render_options()
            elif self.state.is_app_state(APPSTATE.QUIT):
                pygame.quit()
                ex()

            pygame.display.update()
            self.clock.tick(60)

    def start_game(self):
        game = Game(self.state,self)
        game.game_loop()
        print("starting game...")


    def quit(self):
        pygame.quit()
        ex()