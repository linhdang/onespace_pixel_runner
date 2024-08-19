from random import choice

import pygame

from obstacle import Obstacle
from player import Player


class PixelRunner:

    def __init__(self, mode=pygame.display.set_mode((800, 400))) -> None:
        self.score = None
        self.start_time = None
        self.game_active = None
        self.ground_surface = None
        self.sky_surface = None
        self.font = None
        self.screen = None
        self.clock = None
        self.initialize_game_screen(mode)

        # Groups
        self.player = pygame.sprite.GroupSingle()
        self.obstacle_group = pygame.sprite.Group()
        self.player.add(Player())

        self.obstacle_rect_list = []

        # Timer
        self.obstacle_refresh_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_refresh_event, 1500)


    def initialize_game_screen(self, mode):
        self.screen = mode
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('font/Pixeltype.ttf', 50)
        self.sky_surface = pygame.image.load('graphics/Sky.png').convert()
        self.ground_surface = pygame.image.load('graphics/ground.png').convert()
        bg_music = pygame.mixer.Sound('audio/music.wav')
        bg_music.play(loops=-1)
        self.game_active = False
        self.start_time = 0
        self.score = 0

    def get_random_obstacle(self):
        self.obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))


    def start_game(self):
        self.game_active = True
        self.start_time = int(pygame.time.get_ticks() / 1000)


    def draw_player_and_obstacles(self):
        self.draw_background()
        self.player.draw(self.screen)
        self.player.update()

        self.obstacle_group.draw(self.screen)
        self.obstacle_group.update()

    def draw_background(self):
        self.screen.blit(self.sky_surface, (0, 0))
        self.screen.blit(self.ground_surface, (0, 300))


    def run(self):
        self.draw_background()
        while True:
            for event in pygame.event.get():
                # event handler
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                else:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        self.start_game()
                if self.game_active:
                    if event.type == self.obstacle_refresh_event:
                        self.get_random_obstacle()
            if self.game_active:
                self.draw_player_and_obstacles()


            pygame.display.update()
            self.clock.tick(60)
