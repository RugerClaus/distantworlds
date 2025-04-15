import pygame
from core.state.manager import StateManager
from core.state.appstate import APPSTATE
from ui.button import Button

class Menu:
    def __init__(self, state_manager: StateManager,window):
        self.state = state_manager
        self.window = window
        self.screen = window.screen

    def update(self):
        if self.state.is_app_state(APPSTATE.MAIN_MENU):
            self.render_main()
        elif self.state.is_app_state(APPSTATE.OPTIONS_MENU):
            self.render_options()

    def render_main(self):
        button_unhovered_color = "orange"
        button_hovered_color = "white"

        title = pygame.image.load("assets/graphics/menu/DWTitle.png").convert_alpha()
        title_rect = title.get_rect(center = (500,100))

        play_button = Button("Play!", 500, 192, 125, 50, button_unhovered_color, button_hovered_color,
                             self.play_game)
        options_button = Button("Options", 500, 384, 125, 50, button_unhovered_color,
                                button_hovered_color, self.load_options)
        quit_button = Button("Exit", 500, 576, 125, 50, button_unhovered_color, button_hovered_color,
                             self.quit_game)

        self.screen.fill((255, 128, 0))
        self.screen.blit(title,title_rect)
        play_button.draw(self.screen, pygame.mouse.get_pos())
        options_button.draw(self.screen, pygame.mouse.get_pos())
        quit_button.draw(self.screen, pygame.mouse.get_pos())

        pygame.display.flip()

        self.handle_ui_events([play_button, options_button, quit_button])
    
    def play_game(self):
        self.state.set_app_state(APPSTATE.GAME_ACTIVE)
        
    def load_options(self):
        # this will handle the logic for loading the 
        # self.state.set_state(APPSTATE.OPTIONS_MENU)
        pass    
    def quit_game(self):
        self.state.set_app_state(APPSTATE.QUIT)

    def handle_ui_events(self, buttons):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for button in buttons:
                        button.is_clicked(pygame.mouse.get_pos(), event.button == 1)
                elif event.type == pygame.MOUSEMOTION:
                    return
    def render_options(self):
        print("null")

