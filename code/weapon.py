import pygame

from code.player import Player

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        direction = player.status.split('_')[0]
        path = f"./resources/graphics/weapons/{player.weapon_type}/{direction}.png"
        if direction == "up":
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(midbottom=player.rect.midtop)
        elif direction == "down":
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(midtop=player.rect.midbottom)
        elif direction == "right":
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(midleft=player.rect.midright)
        else:
            self.image = pygame.image.load(path)
            self.rect = self.image.get_rect(midright=player.rect.midleft)
        