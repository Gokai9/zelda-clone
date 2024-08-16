import pygame
from code.debug import debug

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('./resources/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 4
        self.obstacles_sprites = sprite

    def input_key(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.direction.y = 1
        elif keys[pygame.K_DOWN]:
            self.direction.y = -1
        else:
            self.direction.y = 0
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, speed):
        # if both x, y value not == 0
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.rect.y -= self.direction.y * speed
        self.collission_detector('vertical')
        self.rect.x += self.direction.x * speed
        self.collission_detector('horizontal')

    def collission_detector(self, direction):
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0:
                        self.rect.top = sprite.rect.bottom
                    if self.direction.y < 0:
                        self.rect.bottom = sprite.rect.top
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = sprite.rect.left
                    if self.direction.x < 0:
                        self.rect.left = sprite.rect.right

    def update(self):
        debug(self.direction.xy)
        self.input_key()
        self.move(self.speed)