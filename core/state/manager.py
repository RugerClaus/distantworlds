from core.state.appstate import APPSTATE

class StateManager:
    def __init__(self, debug=True):
        self.current_state = APPSTATE.MAIN_MENU
        self.previous_state = None
        self.input_locked = False
        self.debug = debug
        self.allowed_transitions = {
            APPSTATE.MAIN_MENU: [APPSTATE.OPTIONS_MENU, APPSTATE.GAME_ACTIVE,APPSTATE.QUIT],
            APPSTATE.OPTIONS_MENU: [APPSTATE.MAIN_MENU],
            APPSTATE.GAME_ACTIVE: [APPSTATE.MAIN_MENU, APPSTATE.OPTIONS_MENU],
            APPSTATE.QUIT: []
        }

    def lock_input(self):
        self.input_locked = True

    def unlock_input(self):
        self.input_locked = False

    def set_state(self, new_state):
        if new_state == self.current_state:
            return  # No change.

        if new_state in self.allowed_transitions.get(self.current_state, []):
            self.previous_state = self.current_state
            self.current_state = new_state

            if self.debug:
                print(f"[STATE] Transitioned: {self.previous_state.name} >>> {self.current_state.name}")

        else:
            if self.debug:
                print(f"[STATE ERROR] Invalid transition: {self.current_state.name} >>> {new_state.name}")

    def is_app_state(self, state):
        return self.current_state == state
