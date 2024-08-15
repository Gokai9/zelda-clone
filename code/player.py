import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, *groups) -> None:
        super().__init__(*groups)
        self.image_player = pygame.image.load('../resources/graphics/test/player.png').convert_alpha()
        self.rect = self.image_player.get_rect(topleft = pos)