
from core.game.world.world import World
import pygame

class IceWorld(World):
    def __init__(self, game):
        super().__init__(game)
    def load_assets(self):
        self.level_bg = pygame.image.load('assets/graphics/game/worlds/1/background.png').convert_alpha()
        self.level_ground = pygame.image.load('assets/graphics/game/worlds/1/ground.jpg').convert_alpha()
