from typing import Any
import pygame
from code.entity import *
from code.help import import_folder
from code.settings import *

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, status) -> None:
        super().__init__(groups)
        self.status = status
        self.animations = {"attack": [], "idle": [], "move": []}
        self.monster_name = monster_name
        self.image_player()
        path = f"./resources/graphics/monsters/{monster_name}/idle/0.png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        #stats
        self.monster_info = monster_data[monster_name]
        self.monster_health = self.monster_info["health"]
    def image_player(self):
        for animation in self.animations.keys():
            path = f"./resources/graphics/monsters/{self.monster_name}/{animation}"
            self.animations[animation] = import_folder(path)
        
    def update(self) -> None:
        self.animate()