from core.state.manager import StateManager
from core.window.window import Window
from core.game.game import Game

if __name__ == "__main__":
    state_manager = StateManager()
    window = Window("v0.1.2", state_manager)

    window.main_loop()