import pygame
from core.state.appstate import APPSTATE
from sys import exit as ex
from ui.menus.menu import Menu
from core.game.game import Game

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
        self.game = Game()
        self.menu = Menu(self.state,self.screen)  # Menu also shares the same state manager

    def main_loop(self):
        while True:
            self.input()

            if self.state.is_app_state(APPSTATE.MAIN_MENU):
                self.menu.render_main()  # you could swap `pass` for real logic
            elif self.state.is_app_state(APPSTATE.GAME_ACTIVE):
                self.start_game()
            elif self.state.is_app_state(APPSTATE.OPTIONS_MENU):
                self.menu.render_options()
            elif self.state.is_app_state(APPSTATE.QUIT):
                pygame.quit()
                ex()

            pygame.display.update()
            self.clock.tick(60)

    def start_game(self):
        # self.game.start()  # Game logic would go here
        print("starting game...")
        
    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                ex()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.screen.fill((255,0,0))