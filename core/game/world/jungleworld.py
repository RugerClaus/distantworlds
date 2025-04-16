import pygame
from core.game.world.world import World

class JungleWorld(World):
    def __init__(self, game):
        super().__init__(game)

    def load_assets(self):
        print("loading level...")
        self.level_bg = pygame.image.load('assets/graphics/game/worlds/2/background.png').convert_alpha()
        self.level_ground = pygame.image.load('assets/graphics/game/worlds/2/ground.jpg').convert_alpha()
