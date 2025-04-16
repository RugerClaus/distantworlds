import pygame
from core.state.appstate import APPSTATE
from core.state.gamestate import *
from ui.menus.pause import PauseMenu
from core.game.levelmanager import LevelManager
from core.game.entities.player import Player
from core.game.entities.door import Door
from util.debug import DebugMenu

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
        self.worlds = ["ice","jungle"]
        self.level_manager = LevelManager(self)
        self.level_manager.load_world(self.worlds[0])
        self.player = Player(self.screen,self,self.window.sound)
        self.door = Door(self.screen)
        self.debug = DebugMenu(self.screen,self.window,self)
        self.door.rect.centerx = 500

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
            

            if self.pause_state:
                self.state.set_game_state(GAMESTATE.PAUSED)
            else:
                self.state.set_game_state(GAMESTATE.PLAYER_INTERACTING)

            if self.state.is_game_state(GAMESTATE.PAUSED):
                self.pause_menu.draw()
            if not self.state.is_game_state(GAMESTATE.PAUSED):
                self.level_manager.update()
                self.level_manager.render()
                self.player.update()
                self.player.draw()
                self.door.draw()
                # print(self.player.rect.left)
                if self.player.rect.colliderect(self.door.rect):
                    self.level_manager.transition_to("jungle")
            if self.debug.on:
                self.debug.update(None)

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
                if event.key == pygame.K_d:
                    self.player.intent = PLAYERSTATE.MOVING_RIGHT
                elif event.key == pygame.K_a:
                    self.player.intent = PLAYERSTATE.MOVING_LEFT
                elif event.key == pygame.K_SPACE:
                    self.player.jump()
                elif event.key == pygame.K_F9:
                    self.debug.toggle()

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_d, pygame.K_a]:
                    self.player.intent = PLAYERSTATE.HOLDING_STILL