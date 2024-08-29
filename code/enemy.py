from typing import Any
import pygame
from code.entity import *
from code.help import import_folder
from code.player import Player
from code.settings import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacles_sprites) -> None:
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.status = 'idle'
        self.animations = {"attack": [], "idle": [], "move": []}
        self.monster_name = monster_name
        self.image_player()
        path = f"./resources/graphics/monsters/{monster_name}/idle/0.png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, 10)
        self.obstacles_sprites = obstacles_sprites
        #stats
        monster_info = monster_data[monster_name]
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.attack_type = monster_info['attack_type']
        self.cooldowns_attack = 600
        self.can_attack = True
        self.attack_time = None
        self.damage_time = None
        self.cooldowns_damage = 300 
        self.accept_damage = True

    def image_player(self):
        for animation in self.animations.keys():
            path = f"./resources/graphics/monsters/{self.monster_name}/{animation}"
            self.animations[animation] = import_folder(path)

    def is_dead(self, player: Player):
        if self.accept_damage:
            self.health -= player.damage_from_player()
            self.accept_damage = False
        print(self.health)
        if self.health < 0:
            self.kill()

    def get_player_distance_direction(self, player: Player):
        vec_player = pygame.math.Vector2(player.rect.center)
        vec_enemy = pygame.math.Vector2(self.rect.center)
        distance = (vec_player - vec_enemy).magnitude()
        if distance > 0:
            direction = (vec_player - vec_enemy).normalize()
        else:
            direction = pygame.math.Vector2()
        return (direction, distance)
    
    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[1]
        if distance <= self.attack_radius and self.can_attack:
            self.status = "attack"
            self.can_attack = False
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"
        
    def actions(self, player):
        direction = self.get_player_distance_direction(player)[0]
        if self.status == "attack":
            self.attack_time = pygame.time.get_ticks()
        elif self.status == "move":
            self.direction = direction
        else:
            self.direction = pygame.math.Vector2()

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.cooldowns_attack:
            self.can_attack = True

    def animate(self):
        animation = self.animations[self.status]
        self.frame += self.animate_time
        if self.frame > len(animation):
            self.frame = 0
        self.image = animation[int(self.frame)]

    def update(self) -> None:
        self.move(self.speed)
        self.animate()
        self.cooldowns

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)
