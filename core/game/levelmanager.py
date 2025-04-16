
class LevelManager:
    def __init__(self, game):
        self.game = game
        self.current_world = None
        self.world_registry = {
            "ice": "core.game.world.iceworld.IceWorld",
            "jungle": "core.game.world.jungleworld.JungleWorld"
        }

    def load_world(self, world_key):
        module_path, class_name = self.world_registry[world_key].rsplit(".", 1)
        mod = __import__(module_path, fromlist=[class_name])
        world_class = getattr(mod, class_name)

        self.current_world = world_class(self.game)
        self.current_world.load_assets()

    def update(self):
        if self.current_world:
            self.current_world.update()

    def render(self):
        if self.current_world:
            self.current_world.render()

    def transition_to(self, world_key):
        # here you could trigger fade-out, cutscene, then swap
        self.game.player.reset()
        self.load_world(world_key)

    def get_background_x(self):
        if self.current_world:
            return getattr(self.current_world, 'background_x', 0)
        return 0