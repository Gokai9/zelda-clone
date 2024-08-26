import pygame
from code.debug import debug
from code.help import import_folder
from code.settings import *
from code.entity import *

class Player(Entity):
    def __init__(self, pos, groups, sprite, set_attack, destroy_weapon) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('./resources/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.animations = {"up": [], "up_attack": [], "up_idle": [],
                            "down": [], "down_attack": [], "down_idle": [], 
                            "right": [], "right_attack": [], "right_idle": [],
                            "left": [], "left_attack": [], "left_idle": []}
        self.image_player()
        self.speed = 7
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = pygame.time.get_ticks()
        self.set_attack = set_attack
        self.destroy_weapon = destroy_weapon
        self.frame = 0
        self.animate_time = 0.15
        #switch weapon
        self.weapon_index = 0
        self.weapon_type = list(weapon_data.keys())[int(self.weapon_index)]
        self.can_switch_weapon = True
        self.weapon_time = pygame.time.get_ticks()
        self.switch_weapon_cooldown = 300
        self.status = "down"
        self.stats = {"health": 100, "mana": 50, "attack": 10, "magic": 5, "speed": 5}
        self.health = self.stats["health"] * 0.7
        self.mana = self.stats["mana"] * 0.9
        self.exp = 123
        self.obstacles_sprites = sprite

    def image_player(self):
        for animation in self.animations.keys():
            self.animations[animation] = import_folder("./resources/graphics/player/" + animation)

    def input_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.status = "up"
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.status = "down"
            self.direction.y = 1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.status = "right"
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.status = "left"
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.set_attack()
            
        if keys[pygame.K_LCTRL] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
        if keys[pygame.K_q] and self.can_switch_weapon:
            self.can_switch_weapon = False
            self.weapon_time = pygame.time.get_ticks()
            if self.weapon_index < len(weapon_data) - 1:
                self.weapon_index += 1
            else:
                self.weapon_index = 0
            self.weapon_type = list(weapon_data.keys())[self.weapon_index]
            
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            if "_attack" in self.status:
                self.status = self.status.replace("_attack", "_idle")
            if "_idle" not in self.status:
                self.status = self.status + "_idle"
        if self.attacking:
            self.status = self.status.replace("_idle", "_attack")
        
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
            self.destroy_weapon()
            self.get_status()
        if current_time - self.weapon_time >= self.switch_weapon_cooldown:
            self.can_switch_weapon = True        

    def animate(self):
        animation = self.animations[self.status]
        self.frame += self.animate_time
        if self.frame > len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]
        #self.rect = self.image.get_rect(topleft = self.)

    def update(self):
        debug(self.status)
        self.input_key()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)