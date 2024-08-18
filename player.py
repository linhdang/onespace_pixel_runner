import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_image_1 = pygame.image.load('graphics/player/player_walk_1.png').convert_alpha()
        player_walk_image_2 = pygame.image.load('graphics/player/player_walk_2.png').convert_alpha()
        self.player_walk_images = [player_walk_image_1, player_walk_image_2]
        self.current_player_image_index = 0

        self.player_jump = pygame.image.load('graphics/player/jump.png').convert_alpha()
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

        self.image = self.player_walk_images[self.current_player_image_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.jump()


    def jump(self):
        self.gravity = -20
        self.jump_sound.play()


    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300


    def walk(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.current_player_image_index += 0.1
            if self.current_player_image_index >= len(self.player_walk_images): self.current_player_image_index = 0
            self.image = self.player_walk_images[int(self.current_player_image_index)]


    def update(self):
        self.player_input()
        self.apply_gravity()
        self.walk()
