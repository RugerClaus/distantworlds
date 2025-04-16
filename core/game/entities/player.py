import pygame
import math
from core.animation.animate import Animation
from core.game.entities.entity import Entity
from core.state.gamestate import PLAYERSTATE

class Player(Entity):
    def __init__(self, screen, game, music_manager):
        super().__init__(screen, has_gravity=True, health=10)
        self.game = game
        self.music_manager = music_manager
        self.speed = 0
        self.intent = PLAYERSTATE.HOLDING_STILL
        self.state = PLAYERSTATE.HOLDING_STILL

        # Inventory and weapons
        self.inventory = {"primary": None, "secondary": None}
        self.active_weapon = None

        # Position and sprite
        self.images = self.load_player_images()
        self.image = self.images["idle"][0]
        self.rect = self.image.get_rect()
        self.rect.bottom = 700
        self.rect.left = 200
        self.world_y = self.rect.bottom -700

        # Setup animations
        self.set_animations()
    
    def reset(self):
        self.rect.bottom = 700
        self.rect.left = 200

    def load_player_images(self):
        return {
            "idle": [pygame.image.load("assets/graphics/game/player/player_stand.png").convert_alpha()],
            "walk_right": [
                pygame.image.load("assets/graphics/game/player/player_walk_1.png").convert_alpha(),
                pygame.image.load("assets/graphics/game/player/player_walk_2.png").convert_alpha()
            ],
            "walk_left": [
                pygame.image.load("assets/graphics/game/player/player_walk_back_1.png").convert_alpha(),
                pygame.image.load("assets/graphics/game/player/player_walk_back_2.png").convert_alpha()
            ],
            "jump_right": [pygame.image.load("assets/graphics/game/player/jump.png").convert_alpha()],
            "jump_left": [pygame.image.load("assets/graphics/game/player/jump_back.png").convert_alpha()],
        }

    def set_animations(self):
        for key, frames in self.images.items():
            self.set_animation(key, Animation(frames, 10))

    def update(self):
        self.world_x = self.rect.centerx
        self.world_y = self.rect.bottom - 700
        super().update()

        self.update_animation()
        self.update_movement()

    def update_animation(self):
        mouse_x = pygame.mouse.get_pos()[0]

        if not self.on_ground:
            self.state = PLAYERSTATE.JUMPING

        if self.state == PLAYERSTATE.JUMPING:
            self.play_animation("jump_right" if self.speed >= 0 else "jump_left")
        elif self.state == PLAYERSTATE.MOVING_RIGHT:
            self.play_animation("walk_right")
        elif self.state == PLAYERSTATE.MOVING_LEFT:
            self.play_animation("walk_left")
        elif mouse_x > self.rect.centerx:
            self.state = PLAYERSTATE.FACING_RIGHT
            self.image = self.images["walk_right"][0]
        elif mouse_x < self.rect.centerx:
            self.state = PLAYERSTATE.FACING_LEFT
            self.image = self.images["walk_left"][0]
        else:
            mouse_x = None
            self.state = PLAYERSTATE.HOLDING_STILL
            self.play_animation("idle")


    def update_movement(self):
        mid_screen = self.screen.get_width() // 2
        self.speed = 0

        if self.intent == PLAYERSTATE.MOVING_RIGHT:
            self.state = PLAYERSTATE.MOVING_RIGHT
            self.speed = 5
        elif self.intent == PLAYERSTATE.MOVING_LEFT:
            self.state = PLAYERSTATE.MOVING_LEFT
            self.speed = -5
        else:
            self.state = PLAYERSTATE.HOLDING_STILL

        if self.rect.left < mid_screen or self.game.level_manager.current_world.background_x in [0, -9000]:
            self.rect.x += self.speed
        else:
            self.rect.x = mid_screen

        if self.rect.x <= 0 or (self.rect.x >= 1000 and self.game.world.background_x <= -9000):
            self.speed = 0
        if self.rect.left <= 0:
            self.rect.left = 0


    def jump(self):
        if self.on_ground:
            self.gravity = -15
            self.on_ground = False
            self.state = PLAYERSTATE.JUMPING
            self.music_manager.play_sfx('jump')
            print("Jumping!")


    def land(self):
        self.on_ground = True
        if self.intent == PLAYERSTATE.MOVING_RIGHT:
            self.state = PLAYERSTATE.MOVING_RIGHT
        elif self.intent == PLAYERSTATE.MOVING_LEFT:
            self.state = PLAYERSTATE.MOVING_LEFT
        else:
            self.state = PLAYERSTATE.HOLDING_STILL

    def rotate_gun_point(self, x, y, angle_deg):
        angle_rad = math.radians(angle_deg)
        cos_theta = math.cos(angle_rad)
        sin_theta = math.sin(angle_rad)
        return (
            x * cos_theta - y * sin_theta,
            x * sin_theta + y * cos_theta
        )

    def draw(self):
        super().draw()
        if self.active_weapon:
            self.draw_weapon()

    def draw_weapon(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.rect.centerx
        dy = mouse_y - self.rect.centery
        angle = math.degrees(math.atan2(dy, dx))

        facing_right = dx >= 0
        self.active_weapon.update_image(facing_right)

        offset_x = 40 if facing_right else -40
        offset_y = 10

        weapon_x = self.rect.centerx + offset_x
        weapon_y = self.rect.centery + offset_y

        rotated_weapon = pygame.transform.rotate(
            self.active_weapon.image, -angle if facing_right else -angle + 180
        )
        weapon_rect = rotated_weapon.get_rect(center=(weapon_x, weapon_y))

        # Update barrel position
        local_offset = (0, 0)  # Customize if needed
        angle_to_use = -angle if facing_right else -angle + 180
        rotated_offset = self.rotate_gun_point(*local_offset, angle_to_use)

        self.active_weapon.barrel_x = weapon_rect.centerx + rotated_offset[0]
        self.active_weapon.barrel_y = weapon_rect.centery + rotated_offset[1]

        self.screen.blit(rotated_weapon, weapon_rect.topleft)

    def switch_weapons(self):
        if self.inventory["primary"] and self.inventory["secondary"]:
            self.active_weapon = (
                self.inventory["primary"]
                if self.active_weapon == self.inventory["secondary"]
                else self.inventory["secondary"]
            )
            self.music_manager.play_sfx(self.active_weapon.pickup_sound)
            print(f"Switched to: {self.active_weapon.canonical_name}")

    def attack(self):
        if self.active_weapon:
            self.active_weapon.use()

    def get_nearest_enemy(self, enemies):
        nearest_enemy = None
        min_distance = float("inf")
        relation = ["", ""]

        for enemy in enemies:
            distance = math.hypot(
                self.rect.centerx - enemy.rect.centerx,
                self.rect.bottom - enemy.rect.bottom
            )
            if distance < min_distance:
                min_distance = distance
                nearest_enemy = enemy

        if nearest_enemy:
            relation[0] = "Left" if nearest_enemy.rect.centerx < self.rect.centerx else "Right"
            if nearest_enemy.rect.top < self.rect.bottom:
                relation[1] = "Up"
            elif nearest_enemy.rect.bottom > self.rect.top:
                relation[1] = "Down"
            elif nearest_enemy.rect.bottom == self.rect.bottom:
                relation[1] = "Level"

            return {
                "position": (nearest_enemy.rect.centerx, nearest_enemy.rect.midbottom[1]),
                "type": nearest_enemy.name,
                "relation_to_player": relation
            }
        return None
