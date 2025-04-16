import pygame

class World:
    def __init__(self, game):
        self.game = game
        self.background_x = 0
        self.background_speed = 3
        self.background_scrolling = False
        self.world_bounds = -12000

    def load_assets(self):
        raise NotImplementedError("Worlds must implement load_assets!")

    def update(self):
        player = self.game.player
        if player.rect.centerx >= 500:
            self.background_scrolling = True
        elif self.background_x == 0:
            self.background_scrolling = False

        if self.background_scrolling:
            if player.speed > 0:
                self.background_x -= self.background_speed
            elif player.speed < 0 and self.background_x < 0:
                self.background_x += self.background_speed

        if self.background_x <= self.world_bounds:
            self.background_scrolling = False
            player.rect.x += player.speed

    def render(self):
        screen = self.game.screen
        screen.blit(self.level_bg, (self.background_x, 0))
        screen.blit(self.level_ground, (self.background_x, 700))
