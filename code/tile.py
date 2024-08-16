import pygame, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups) -> None:
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join('./resources/graphics/test', 'rock.png')).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)