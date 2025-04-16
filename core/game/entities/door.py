import pygame
from core.game.entities.entity import Entity

class Door(Entity):
    def __init__(self, screen, has_gravity=False, health=0):
        super().__init__(screen, has_gravity, health)
        self.image = pygame.image.load('assets/graphics/game/interactibles/door.png')
        self.rect = self.image.get_rect()
        self.rect.bottom = 700
    
    def draw(self):
        self.screen.blit(self.image,self.rect)
