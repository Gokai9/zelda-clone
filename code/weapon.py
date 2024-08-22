import pygame

from code.player import Player

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player: Player, groups) -> None:
        super().__init__(groups)
        self.image = pygame.surface.Surface((40, 40))
        self.rect = self.image.get_rect(center=player.rect.center)