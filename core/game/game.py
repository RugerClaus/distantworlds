import pygame
from core.state.appstate import APPSTATE
from core.state.gamestate import *
from ui.menus.pause import PauseMenu

class Game:
    def __init__(self, state_manager, window):
        self.state = state_manager
        self.window = window
        self.screen = window.screen
        self.color = "white"
        self.pause_state = False
        self.running = True
        self.pause_menu = PauseMenu(
            window,
            self.toggle_pause,
            self.toggle_music,
            self.toggle_sfx,
            self.go_to_main_menu,
            self.window.quit
        )

    def toggle_music(self):
        self.window.sound.toggle_music("game")
        self.pause_menu.update_labels()

    def toggle_sfx(self):
        self.window.sound.toggle_sfx()
        self.pause_menu.update_labels()

    def go_to_main_menu(self):
        self.window.sound.stop_music()
        self.state.set_app_state(APPSTATE.MAIN_MENU)
        self.running = False

    def toggle_pause(self):
        self.pause_state = not self.pause_state

    def game_loop(self):
        self.window.sound.play_music("game")
        while self.running:
            self.input()
            self.screen.fill(self.color)

            if self.pause_state:
                self.state.set_game_state(GAMESTATE.PAUSED)
            else:
                self.state.set_game_state(GAMESTATE.PLAYER_INTERACTING)

            if self.state.is_game_state(GAMESTATE.PAUSED):
                self.pause_menu.draw()

            pygame.display.flip()
            self.window.clock.tick(60)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.window.quit()

            if self.state.is_game_state(GAMESTATE.PAUSED):
                self.pause_menu.handle_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.toggle_pause()
                if event.key == pygame.K_1:
                    self.color = "red"
                if event.key == pygame.K_2:
                    self.color = "white"
