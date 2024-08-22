import pygame
from code.debug import debug
from code.help import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite, set_attack) -> None:
        super().__init__(groups)
        self.image = pygame.image.load('./resources/graphics/test/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -26)
        self.animations = {"up": [], "up_attack": [], "up_idle": [],
                            "down": [], "down_attack": [], "down_idle": [], 
                            "right": [], "right_attack": [], "right_idle": [],
                            "left": [], "left_attack": [], "left_idle": []}
        self.image_player()
        self.direction = pygame.math.Vector2()
        self.speed = 7
        self.attacking = False
        self.attack_cooldown = 1000
        self.attack_time = pygame.time.get_ticks()
        self.set_attack = set_attack
        self.status = "down"
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
            
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0 and not self.attacking:
            if "_attack" in self.status:
                self.status = self.status.replace("_attack", "_idle")
            if "_idle" not in self.status:
                self.status = self.status + "_idle"
        if self.attacking:
            self.status = self.status.replace("_idle", "_attack")
        
    def move(self, speed):
        # if both x, y value not == 0
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()
        self.hitbox.y += self.direction.y * speed
        self.collission_detector('vertical')
        self.hitbox.x += self.direction.x * speed
        self.collission_detector('horizontal')
        self.rect.center = self.hitbox.center

    def collission_detector(self, direction):
        if direction == 'vertical':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top = sprite.hitbox.bottom
        if direction == 'horizontal':
            for sprite in self.obstacles_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right
    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
            self.get_status()

    def update(self):
        debug(self.status)
        self.input_key()
        self.cooldowns()
        self.get_status()
        self.move(self.speed)